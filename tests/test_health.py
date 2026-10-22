from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "mnemora-ai"


def test_create_and_list_memory_entries():
    payload = {
        "title": "Cours Python",
        "content": "Fichiers et tests pour comprendre le projet.",
        "memory_type": "note",
        "source": "user",
    }

    created = client.post("/memory/", json=payload)
    assert created.status_code == 200, created.text
    body = created.json()
    assert body["title"] == payload["title"]
    assert body["memory_type"] == payload["memory_type"]

    listed = client.get("/memory/")
    assert listed.status_code == 200, listed.text
    data = listed.json()
    assert any(item["title"] == payload["title"] for item in data)


def test_create_course_note_project_and_task():
    course_payload = {"name": "Python avancé", "description": "Méthodes et tests"}
    course = client.post("/courses/", json=course_payload)
    assert course.status_code == 200, course.text
    course_id = course.json()["id"]

    note_payload = {
        "title": "Fichiers utiles",
        "content": "On travaille sur le système de mémoire.",
        "course_id": course_id,
    }
    note = client.post("/notes/", json=note_payload)
    assert note.status_code == 200, note.text
    assert note.json()["course_id"] == course_id

    project_payload = {"name": "MNEMORA IA", "description": "Projet mémoire perso", "status": "active"}
    project = client.post("/projects/", json=project_payload)
    assert project.status_code == 200, project.text
    project_id = project.json()["id"]

    task_payload = {
        "title": "Rédiger le README",
        "description": "Documenter la base du projet.",
        "status": "todo",
        "project_id": project_id,
    }
    task = client.post("/tasks/", json=task_payload)
    assert task.status_code == 200, task.text
    assert task.json()["project_id"] == project_id

    assert client.get("/courses/").status_code == 200
    assert client.get("/notes/").status_code == 200
    assert client.get("/projects/").status_code == 200
    assert client.get("/tasks/").status_code == 200


def test_memory_search_and_relations():
    first = client.post(
        "/memory/",
        json={
            "title": "Mémoire Python",
            "content": "Les tests automatiques permettent de valider le code rapidement.",
            "memory_type": "note",
            "source": "user",
        },
    )
    second = client.post(
        "/memory/",
        json={
            "title": "Tests automatisés",
            "content": "La validation continue est essentielle pour la qualité logicielle.",
            "memory_type": "note",
            "source": "assistant",
        },
    )

    assert first.status_code == 200, first.text
    assert second.status_code == 200, second.text

    link = client.post(
        "/memory/relations/",
        json={"source_id": first.json()["id"], "target_id": second.json()["id"], "relation_type": "related"},
    )
    assert link.status_code == 200, link.text
    assert link.json()["relation_type"] == "related"

    results = client.get("/memory/search?query=tests")
    assert results.status_code == 200, results.text
    assert any(item["title"] == "Mémoire Python" for item in results.json())
