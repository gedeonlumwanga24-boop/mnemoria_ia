from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models import Course, MemoryEntry, MemoryRelation, Note, Project, Task
from app.schemas import (
    CourseCreate,
    CourseUpdate,
    MemoryEntryCreate,
    MemoryRelationCreate,
    NoteCreate,
    NoteUpdate,
    ProjectCreate,
    ProjectUpdate,
    TaskCreate,
    TaskUpdate,
)


def get_memory_entry(db: Session, memory_id: int):
    return db.query(MemoryEntry).filter(MemoryEntry.id == memory_id).first()


def create_memory_entry(db: Session, payload: MemoryEntryCreate) -> MemoryEntry:
    item = MemoryEntry(
        title=payload.title,
        content=payload.content,
        memory_type=payload.memory_type,
        source=payload.source,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_memory_entry(db: Session, memory_id: int, payload: MemoryEntryCreate):
    item = get_memory_entry(db, memory_id)
    if not item:
        return None
    item.title = payload.title
    item.content = payload.content
    item.memory_type = payload.memory_type
    item.source = payload.source
    db.commit()
    db.refresh(item)
    return item


def delete_memory_entry(db: Session, memory_id: int):
    item = get_memory_entry(db, memory_id)
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True


def list_memory_entries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MemoryEntry).order_by(MemoryEntry.created_at.desc()).offset(skip).limit(limit).all()


def search_memory_entries(db: Session, query: str, skip: int = 0, limit: int = 50):
    if not query or not query.strip():
        return list_memory_entries(db, skip=skip, limit=limit)

    term = f"%{query.strip()}%"
    return (
        db.query(MemoryEntry)
        .filter(or_(MemoryEntry.title.ilike(term), MemoryEntry.content.ilike(term)))
        .order_by(MemoryEntry.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_memory_relation(db: Session, payload: MemoryRelationCreate) -> MemoryRelation:
    item = MemoryRelation(
        source_id=payload.source_id,
        target_id=payload.target_id,
        relation_type=payload.relation_type,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_memory_relations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MemoryRelation).order_by(MemoryRelation.created_at.desc()).offset(skip).limit(limit).all()


def list_memory_relations_for_entry(db: Session, memory_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(MemoryRelation)
        .filter(or_(MemoryRelation.source_id == memory_id, MemoryRelation.target_id == memory_id))
        .order_by(MemoryRelation.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_course(db: Session, payload: CourseCreate) -> Course:
    item = Course(name=payload.name, description=payload.description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Course).order_by(Course.created_at.desc()).offset(skip).limit(limit).all()


def get_course(db: Session, course_id: int):
    return db.query(Course).filter(Course.id == course_id).first()


def update_course(db: Session, course_id: int, payload: CourseUpdate):
    item = get_course(db, course_id)
    if not item:
        return None
    item.name = payload.name
    item.description = payload.description
    db.commit()
    db.refresh(item)
    return item


def delete_course(db: Session, course_id: int):
    item = get_course(db, course_id)
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True


def create_note(db: Session, payload: NoteCreate) -> Note:
    item = Note(title=payload.title, content=payload.content, course_id=payload.course_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_notes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Note).order_by(Note.created_at.desc()).offset(skip).limit(limit).all()


def list_notes_by_course(db: Session, course_id: int, skip: int = 0, limit: int = 100):
    return db.query(Note).filter(Note.course_id == course_id).order_by(Note.created_at.desc()).offset(skip).limit(limit).all()


def get_note(db: Session, note_id: int):
    return db.query(Note).filter(Note.id == note_id).first()


def update_note(db: Session, note_id: int, payload: NoteUpdate):
    item = get_note(db, note_id)
    if not item:
        return None
    item.title = payload.title
    item.content = payload.content
    item.course_id = payload.course_id
    db.commit()
    db.refresh(item)
    return item


def delete_note(db: Session, note_id: int):
    item = get_note(db, note_id)
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True


def create_project(db: Session, payload: ProjectCreate) -> Project:
    item = Project(name=payload.name, description=payload.description, status=payload.status)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Project).order_by(Project.created_at.desc()).offset(skip).limit(limit).all()


def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


def update_project(db: Session, project_id: int, payload: ProjectUpdate):
    item = get_project(db, project_id)
    if not item:
        return None
    item.name = payload.name
    item.description = payload.description
    item.status = payload.status
    db.commit()
    db.refresh(item)
    return item


def delete_project(db: Session, project_id: int):
    item = get_project(db, project_id)
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True


def create_task(db: Session, payload: TaskCreate) -> Task:
    item = Task(
        title=payload.title,
        description=payload.description,
        status=payload.status,
        project_id=payload.project_id,
        due_date=payload.due_date,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Task).order_by(Task.created_at.desc()).offset(skip).limit(limit).all()


def list_tasks_by_project(db: Session, project_id: int, skip: int = 0, limit: int = 100):
    return db.query(Task).filter(Task.project_id == project_id).order_by(Task.created_at.desc()).offset(skip).limit(limit).all()


def get_project_summary(db: Session, project_id: int):
    item = get_project(db, project_id)
    if not item:
        return None

    tasks = list_tasks_by_project(db, project_id)
    completed_tasks = sum(1 for task in tasks if str(task.status).lower() in {"done", "completed", "closed"})
    pending_tasks = len(tasks) - completed_tasks

    return {
        "project_id": item.id,
        "project_name": item.name,
        "status": item.status,
        "total_tasks": len(tasks),
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
    }


def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def update_task(db: Session, task_id: int, payload: TaskUpdate):
    item = get_task(db, task_id)
    if not item:
        return None
    item.title = payload.title
    item.description = payload.description
    item.status = payload.status
    item.project_id = payload.project_id
    item.due_date = payload.due_date
    db.commit()
    db.refresh(item)
    return item


def delete_task(db: Session, task_id: int):
    item = get_task(db, task_id)
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True
