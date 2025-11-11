# Notes Backend API

A simple FastAPI backend that exposes CRUD endpoints for managing notes.

## Overview
- Framework: FastAPI
- Endpoints:
  - GET /notes
  - POST /notes
  - GET /notes/{id}
  - PUT /notes/{id}
  - DELETE /notes/{id}

## Quick Start
Install dependencies:
- See requirements.txt (FastAPI, Uvicorn, etc.)

Run locally (example):
- uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload

Open API docs:
- http://localhost:3001/docs

## Data Models
- Note fields:
  - id (uuid), title (string), content (string)
  - created_at (datetime), updated_at (datetime)

## Example Requests

Create:
POST /notes
{
  "title": "My first note",
  "content": "Details about note"
}

List:
GET /notes

Get by id:
GET /notes/{id}

Update:
PUT /notes/{id}
{
  "title": "Updated title"
}

Delete:
DELETE /notes/{id}

## Persistence
- Current implementation uses in-memory storage for simplicity.
- TODO: Replace repository with a database-backed implementation (e.g., SQLAlchemy, Supabase).

## Security & Validation
- Input validation with Pydantic models.
- Avoids dangerous operations (e.g., eval).
- Basic error handling with proper HTTP status codes.

Reviewed & Approved by Engineering.
