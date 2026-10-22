from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MemoryEntryBase(BaseModel):
    title: str
    content: str
    memory_type: str = "note"
    source: str = "user"


class MemoryEntryCreate(MemoryEntryBase):
    pass


class MemoryEntryRead(MemoryEntryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MemoryRelationBase(BaseModel):
    source_id: int
    target_id: int
    relation_type: str = "related"


class MemoryRelationCreate(MemoryRelationBase):
    pass


class MemoryRelationRead(MemoryRelationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CourseBase(BaseModel):
    name: str
    description: str = ""


class CourseCreate(CourseBase):
    pass


class CourseUpdate(CourseBase):
    pass


class CourseRead(CourseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NoteBase(BaseModel):
    title: str
    content: str
    course_id: int | None = None


class NoteCreate(NoteBase):
    pass


class NoteUpdate(NoteBase):
    pass


class NoteRead(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectBase(BaseModel):
    name: str
    description: str = ""
    status: str = "planned"


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskBase(BaseModel):
    title: str
    description: str = ""
    status: str = "todo"
    project_id: int | None = None
    due_date: datetime | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
