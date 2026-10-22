from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.crud import (
    create_course,
    create_memory_entry,
    create_memory_relation,
    create_note,
    create_project,
    create_task,
    delete_course,
    delete_memory_entry,
    delete_note,
    delete_project,
    delete_task,
    get_course,
    get_memory_entry,
    get_note,
    get_project,
    get_project_summary,
    get_task,
    list_courses,
    list_memory_entries,
    list_memory_relations,
    list_memory_relations_for_entry,
    list_notes,
    list_notes_by_course,
    list_projects,
    list_tasks,
    list_tasks_by_project,
    search_memory_entries,
    update_course,
    update_memory_entry,
    update_note,
    update_project,
    update_task,
)
from app.database import get_db, init_db
from app.models import MemoryEntry
from app.schemas import (
    CourseCreate,
    CourseRead,
    CourseUpdate,
    MemoryEntryCreate,
    MemoryEntryRead,
    MemoryRelationCreate,
    MemoryRelationRead,
    NoteCreate,
    NoteRead,
    NoteUpdate,
    ProjectCreate,
    ProjectRead,
    ProjectSummary,
    ProjectUpdate,
    TaskCreate,
    TaskRead,
    TaskUpdate,
)


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="MNEMORA AI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

init_db()


@app.get("/")
def serve_frontend():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "mnemora-ai",
    }


@app.post("/memory/", response_model=MemoryEntryRead)
def add_memory_entry(payload: MemoryEntryCreate, db: Session = Depends(get_db)):
    return create_memory_entry(db, payload)


@app.get("/memory/", response_model=list[MemoryEntryRead])
def get_memory_entries(db: Session = Depends(get_db)):
    return list_memory_entries(db)


@app.get("/memory/search", response_model=list[MemoryEntryRead])
def search_memory(query: str, db: Session = Depends(get_db)):
    return search_memory_entries(db, query)


@app.get("/memory/relations/", response_model=list[MemoryRelationRead])
def get_memory_relations(db: Session = Depends(get_db)):
    return list_memory_relations(db)


@app.get("/memory/{memory_id}", response_model=MemoryEntryRead)
def get_memory_detail(memory_id: int, db: Session = Depends(get_db)):
    item = get_memory_entry(db, memory_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory item not found")
    return item


@app.put("/memory/{memory_id}", response_model=MemoryEntryRead)
def edit_memory_entry(memory_id: int, payload: MemoryEntryCreate, db: Session = Depends(get_db)):
    item = update_memory_entry(db, memory_id, payload)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory item not found")
    return item


@app.delete("/memory/{memory_id}")
def remove_memory_entry(memory_id: int, db: Session = Depends(get_db)):
    if not delete_memory_entry(db, memory_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory item not found")
    return {"ok": True, "deleted_id": memory_id}


@app.get("/memory/{memory_id}/relations", response_model=list[MemoryRelationRead])
def get_memory_entry_relations(memory_id: int, db: Session = Depends(get_db)):
    item = get_memory_entry(db, memory_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory item not found")
    return list_memory_relations_for_entry(db, memory_id)


@app.post("/memory/relations/", response_model=MemoryRelationRead)
def add_memory_relation(payload: MemoryRelationCreate, db: Session = Depends(get_db)):
    source = db.query(MemoryEntry).filter(MemoryEntry.id == payload.source_id).first()
    target = db.query(MemoryEntry).filter(MemoryEntry.id == payload.target_id).first()
    if not source or not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory item not found")
    if payload.source_id == payload.target_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A memory item cannot relate to itself")
    return create_memory_relation(db, payload)


@app.post("/courses/", response_model=CourseRead)
def add_course(payload: CourseCreate, db: Session = Depends(get_db)):
    return create_course(db, payload)


@app.get("/courses/", response_model=list[CourseRead])
def get_courses(db: Session = Depends(get_db)):
    return list_courses(db)


@app.get("/courses/{course_id}", response_model=CourseRead)
def get_course_detail(course_id: int, db: Session = Depends(get_db)):
    item = get_course(db, course_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return item


@app.get("/courses/{course_id}/notes", response_model=list[NoteRead])
def get_course_notes(course_id: int, db: Session = Depends(get_db)):
    item = get_course(db, course_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return list_notes_by_course(db, course_id)


@app.put("/courses/{course_id}", response_model=CourseRead)
def edit_course(course_id: int, payload: CourseUpdate, db: Session = Depends(get_db)):
    item = update_course(db, course_id, payload)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return item


@app.delete("/courses/{course_id}")
def remove_course(course_id: int, db: Session = Depends(get_db)):
    if not delete_course(db, course_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return {"ok": True, "deleted_id": course_id}


@app.post("/notes/", response_model=NoteRead)
def add_note(payload: NoteCreate, db: Session = Depends(get_db)):
    return create_note(db, payload)


@app.get("/notes/", response_model=list[NoteRead])
def get_notes(db: Session = Depends(get_db)):
    return list_notes(db)


@app.get("/notes/{note_id}", response_model=NoteRead)
def get_note_detail(note_id: int, db: Session = Depends(get_db)):
    item = get_note(db, note_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return item


@app.put("/notes/{note_id}", response_model=NoteRead)
def edit_note(note_id: int, payload: NoteUpdate, db: Session = Depends(get_db)):
    item = update_note(db, note_id, payload)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return item


@app.delete("/notes/{note_id}")
def remove_note(note_id: int, db: Session = Depends(get_db)):
    if not delete_note(db, note_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return {"ok": True, "deleted_id": note_id}


@app.post("/projects/", response_model=ProjectRead)
def add_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    return create_project(db, payload)


@app.get("/projects/", response_model=list[ProjectRead])
def get_projects(db: Session = Depends(get_db)):
    return list_projects(db)


@app.get("/projects/{project_id}", response_model=ProjectRead)
def get_project_detail(project_id: int, db: Session = Depends(get_db)):
    item = get_project(db, project_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return item


@app.get("/projects/{project_id}/summary", response_model=ProjectSummary)
def project_summary(project_id: int, db: Session = Depends(get_db)):
    item = get_project_summary(db, project_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return item


@app.get("/projects/{project_id}/tasks", response_model=list[TaskRead])
def project_tasks(project_id: int, db: Session = Depends(get_db)):
    item = get_project(db, project_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return list_tasks_by_project(db, project_id)


@app.put("/projects/{project_id}", response_model=ProjectRead)
def edit_project(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db)):
    item = update_project(db, project_id, payload)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return item


@app.delete("/projects/{project_id}")
def remove_project(project_id: int, db: Session = Depends(get_db)):
    if not delete_project(db, project_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return {"ok": True, "deleted_id": project_id}


@app.post("/tasks/", response_model=TaskRead)
def add_task(payload: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, payload)


@app.get("/tasks/", response_model=list[TaskRead])
def get_tasks(db: Session = Depends(get_db)):
    return list_tasks(db)


@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task_detail(task_id: int, db: Session = Depends(get_db)):
    item = get_task(db, task_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return item


@app.put("/tasks/{task_id}", response_model=TaskRead)
def edit_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    item = update_task(db, task_id, payload)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return item


@app.delete("/tasks/{task_id}")
def remove_task(task_id: int, db: Session = Depends(get_db)):
    if not delete_task(db, task_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return {"ok": True, "deleted_id": task_id}
