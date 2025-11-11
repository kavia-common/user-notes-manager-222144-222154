from __future__ import annotations

from datetime import datetime
from typing import Dict, List
from uuid import UUID

from ..models import Note, NoteCreate, NoteUpdate


class NotFoundError(Exception):
    """Raised when a Note is not found in the repository."""


class ValidationError(Exception):
    """Raised when a validation error occurs at the repository layer."""


class NotesRepository:
    """
    In-memory repository for Note entities.
    This uses a process-local dictionary for storage and is NOT durable.

    TODO: Replace with real database-backed implementation (e.g., SQLAlchemy or Supabase).
    """

    def __init__(self) -> None:
        # Using a dict keyed by UUID for O(1) access.
        self._store: Dict[UUID, Note] = {}

    def list_notes(self) -> List[Note]:
        """Return all notes sorted by created_at ascending."""
        return sorted(self._store.values(), key=lambda n: n.created_at)

    def create_note(self, payload: NoteCreate) -> Note:
        """Create and store a new note."""
        note = Note.new_from_create(payload)
        self._store[note.id] = note
        return note

    def get_note(self, note_id: UUID) -> Note:
        """Retrieve a note by ID."""
        note = self._store.get(note_id)
        if not note:
            raise NotFoundError(f"Note with id {note_id} not found")
        return note

    def update_note(self, note_id: UUID, payload: NoteUpdate) -> Note:
        """Update an existing note with provided fields."""
        note = self.get_note(note_id)

        # Validate at least one field is being updated
        if payload.title is None and payload.content is None:
            raise ValidationError("At least one of 'title' or 'content' must be provided")

        updated = note.model_copy(update={
            "title": payload.title if payload.title is not None else note.title,
            "content": payload.content if payload.content is not None else note.content,
            "updated_at": datetime.utcnow(),
        })
        self._store[note_id] = updated
        return updated

    def delete_note(self, note_id: UUID) -> None:
        """Delete a note by ID."""
        if note_id not in self._store:
            raise NotFoundError(f"Note with id {note_id} not found")
        del self._store[note_id]


# Simple singleton-style repository instance for app-wide use.
# PUBLIC_INTERFACE
def get_repository() -> NotesRepository:
    """Return the global NotesRepository instance."""
    # Using a function-level global to avoid issues with import order.
    global _GLOBAL_NOTES_REPOSITORY  # type: ignore
    try:
        repo = _GLOBAL_NOTES_REPOSITORY  # type: ignore
    except NameError:
        _GLOBAL_NOTES_REPOSITORY = NotesRepository()  # type: ignore
        repo = _GLOBAL_NOTES_REPOSITORY  # type: ignore
    return repo
