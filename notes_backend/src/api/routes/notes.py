from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status
from fastapi.responses import JSONResponse

from ..models import Note, NoteCreate, NoteUpdate
from ..repositories.notes_repo import NotFoundError, ValidationError, NotesRepository, get_repository

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.get(
    "",
    response_model=List[Note],
    summary="List notes",
    description="Retrieve a list of all notes.",
    responses={
        200: {"description": "A list of notes."},
    },
)
# PUBLIC_INTERFACE
def list_notes(repo: NotesRepository = Depends(get_repository)) -> List[Note]:
    """Return all notes.

    Returns:
        List[Note]: All notes in the repository ordered by created_at ascending.

    Example:
        GET /notes
        Response 200: [{"id":"<uuid>","title":"T","content":"C","created_at":"...","updated_at":"..."}]
    """
    return repo.list_notes()


@router.post(
    "",
    response_model=Note,
    status_code=status.HTTP_201_CREATED,
    summary="Create note",
    description="Create a new note with title and content.",
    responses={
        201: {"description": "Note created successfully."},
        400: {"description": "Invalid payload."},
    },
)
# PUBLIC_INTERFACE
def create_note(payload: NoteCreate, repo: NotesRepository = Depends(get_repository)) -> Note:
    """Create a new note.

    Args:
        payload (NoteCreate): Title and content for the note.

    Returns:
        Note: The created note including id and timestamps.

    Example:
        POST /notes
        Body: {"title":"My Note", "content":"Details"}
        Response 201: {"id":"<uuid>","title":"My Note","content":"Details","created_at":"...","updated_at":"..."}
    """
    try:
        return repo.create_note(payload)
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get(
    "/{note_id}",
    response_model=Note,
    summary="Get note",
    description="Get a specific note by its ID.",
    responses={
        200: {"description": "Note found and returned."},
        404: {"description": "Note not found."},
    },
)
# PUBLIC_INTERFACE
def get_note(
    note_id: UUID = Path(..., description="UUID of the note"),
    repo: NotesRepository = Depends(get_repository),
) -> Note:
    """Retrieve a single note by id.

    Args:
        note_id (UUID): The note's unique identifier.

    Returns:
        Note: The requested note if it exists.
    """
    try:
        return repo.get_note(note_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put(
    "/{note_id}",
    response_model=Note,
    summary="Update note",
    description="Update a note's title and/or content by its ID.",
    responses={
        200: {"description": "Note updated successfully."},
        400: {"description": "Invalid payload."},
        404: {"description": "Note not found."},
    },
)
# PUBLIC_INTERFACE
def update_note(
    note_id: UUID = Path(..., description="UUID of the note"),
    payload: NoteUpdate = ...,
    repo: NotesRepository = Depends(get_repository),
) -> Note:
    """Update a note by id.

    Args:
        note_id (UUID): The note ID.
        payload (NoteUpdate): Fields to update.

    Returns:
        Note: The updated note.
    """
    try:
        return repo.update_note(note_id, payload)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete note",
    description="Delete a note by its ID.",
    responses={
        204: {"description": "Note deleted."},
        404: {"description": "Note not found."},
    },
)
# PUBLIC_INTERFACE
def delete_note(
    note_id: UUID = Path(..., description="UUID of the note"),
    repo: NotesRepository = Depends(get_repository),
) -> JSONResponse:
    """Delete a note by id.

    Args:
        note_id (UUID): The note ID.

    Returns:
        JSONResponse: Empty response with 204 status.
    """
    try:
        repo.delete_note(note_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    # For 204 response, return an empty response body
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
