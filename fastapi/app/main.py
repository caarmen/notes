from typing import Annotated

import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import crud
from app.database.session import get_session
from app.service.model import Note
from fastapi import Body, Depends, FastAPI, status

app = FastAPI()


@app.post("/notes/", status_code=status.HTTP_201_CREATED)
async def create_note(
    text: Annotated[str, Body(embed=True)], session: AsyncSession = Depends(get_session)
) -> Note:
    return await crud.create_note(session, text)


@app.get("/notes/")
async def list_notes(session: AsyncSession = Depends(get_session)) -> list[Note]:
    return await crud.list_notes(session)


@app.get("/notes/{note_id}")
async def get_note(note_id: int, session: AsyncSession = Depends(get_session)) -> Note:
    return await crud.get_note(session, id=note_id)


@app.put("/notes/{note_id}")
async def update_note(
    note_id: int,
    text: Annotated[str, Body(embed=True)],
    session: AsyncSession = Depends(get_session),
) -> Note:
    return await crud.update_note(session, id=note_id, new_text=text)


@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    session: AsyncSession = Depends(get_session),
) -> None:
    await crud.delete_note(session, id=note_id)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
