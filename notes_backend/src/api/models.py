from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


# PUBLIC_INTERFACE
class NoteBase(BaseModel):
    """Base fields for a Note object used in create/update operations."""

    title: str = Field(..., description="Title of the note", min_length=1, max_length=200)
    content: str = Field(..., description="Content/body of the note", min_length=1)


# PUBLIC_INTERFACE
class NoteCreate(NoteBase):
    """Payload model for creating a new note."""
    pass


# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Payload model for updating an existing note."""
    title: Optional[str] = Field(None, description="Updated title of the note", min_length=1, max_length=200)
    content: Optional[str] = Field(None, description="Updated content of the note", min_length=1)


# PUBLIC_INTERFACE
class Note(NoteBase):
    """Response model representing a Note."""
    id: UUID = Field(..., description="Unique identifier for the note")
    created_at: datetime = Field(..., description="Timestamp when the note was created (UTC)")
    updated_at: datetime = Field(..., description="Timestamp when the note was last updated (UTC)")

    @staticmethod
    def new_from_create(data: NoteCreate) -> "Note":
        """Create a new Note instance from NoteCreate with generated id and timestamps."""
        now = datetime.utcnow()
        return Note(
            id=uuid4(),
            title=data.title,
            content=data.content,
            created_at=now,
            updated_at=now,
        )


# PUBLIC_INTERFACE
class MessageResponse(BaseModel):
    """Standard message response model."""
    message: str = Field(..., description="Informational message about the operation result")
