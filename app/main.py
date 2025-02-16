import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.config import settings
from bot.handlers import get_routers
from bot.database.crud.tasks import test_connection
from bot.middlewares import DataBaseSession


logger = logging.getLogger(__name__)


async def main():

    engine = create_async_engine(url=str(settings.db.url))
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async with session_maker() as session:
        await test_connection(session)
        logger.info("Test connect database")

    bot: Bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp: Dispatcher = Dispatcher()
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    dp.include_routers(*get_routers())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
