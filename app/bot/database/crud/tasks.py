from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Task


async def get_task_by_id(session: AsyncSession, id_task: int) -> Task | None:
    stmt = select(Task).where(Task.id == id_task)
    return await session.scalar(stmt)


async def create_task(session: AsyncSession, text: str) -> None:
    task = Task(text=text)
    session.add(task)
    await session.commit()


async def get_all_tasks(session: AsyncSession) -> list[Task]:
    stmt = select(Task)
    result = await session.scalars(stmt)
    return result.all()


async def test_connection(session: AsyncSession):
    """
    Проверка соединения с СУБД
    """
    stmt = select(1)
    return await session.scalar(stmt)
