from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from app import models, schemas, auth
from typing import List

router = APIRouter()

@router.post("/notes/", response_model=schemas.Note)  # MongoDB (Beanie)
async def create_note(
    note: schemas.NoteCreate, current_user: models.User = Depends(auth.get_current_user)
):
    db_note = models.Note(**note.model_dump(), user_id=current_user.user_id)
    await db_note.insert()
    return db_note


@router.get("/notes/", response_model=List[schemas.Note])  # MongoDB (Beanie)
async def read_notes(current_user: models.User = Depends(auth.get_current_user)):
    notes = await models.Note.find(models.Note.user_id == current_user.user_id).to_list()
    return notes

@router.put("/notes/{note_id}", response_model=schemas.Note)  # MongoDB (Beanie)
async def update_note(
    note_id: str,
    note_update: schemas.NoteUpdate,
    current_user: models.User = Depends(auth.get_current_user),
):
    note = await models.Note.find_one(models.Note.note_id == note_id)
    if not note or str(note.user_id) != str(current_user.user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    note_update_dict = note_update.model_dump(exclude_unset=True)
    if note_update_dict:
        note.last_update = datetime.utcnow()
        await note.update({"$set": note_update_dict})
    await note.reload()
    return note


@router.delete("/notes/{note_id}", response_model=schemas.Note)  # MongoDB (Beanie)
async def delete_note(
    note_id: str, current_user: models.User = Depends(auth.get_current_user)
):
    note = await models.Note.find_one(models.Note.note_id == note_id)
    if not note or str(note.user_id) != str(current_user.user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    await note.delete()
    return note