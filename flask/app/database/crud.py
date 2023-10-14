from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import model


async def create_note(session: AsyncSession, text: str) -> model.Note:
    note = model.Note(text=text)
    session.add(note)
    await session.commit()
    await session.refresh(note)
    return note


async def list_notes(session: AsyncSession) -> list[model.Note]:
    return (await session.scalars(statement=select(model.Note))).all()


async def get_note(session: AsyncSession, id: int) -> model.Note:
    return (
        await session.scalars(statement=select(model.Note).where(model.Note.id == id))
    ).one()


async def update_note(session: AsyncSession, id: int, new_text: str) -> model.Note:
    await session.execute(
        statement=update(model.Note).where(model.Note.id == id).values(text=new_text)
    )
    await session.commit()
    return await get_note(session, id)


async def delete_note(session: AsyncSession, id: int) -> model.Note:
    await session.execute(statement=delete(model.Note).where(model.Note.id == id))
    await session.commit()
