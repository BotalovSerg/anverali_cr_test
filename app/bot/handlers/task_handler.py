from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.states import TaskSG
from bot.keyboards.inline_kb import save_task_kb
from bot.database.crud.tasks import create_task

router = Router()


@router.message(Command("add"))
async def processing_cmd_add(message: Message, state: FSMContext) -> None:
    """Handler"""
    await state.set_state(TaskSG.text)
    await message.answer(
        text="Вы находитесь в режиме добавления задачь, для продолжения введите текс задачи и отправте сообщение."
    )


@router.message(TaskSG.text, F.text)
async def processing_add_task(message: Message, state: FSMContext) -> None:

    await state.update_data(text=message.text)
    await state.set_state(TaskSG.check_task)
    await message.answer(
        text=f"Вы ввели:\n--------\n{message.text}",
        reply_markup=save_task_kb(),
    )


@router.callback_query(TaskSG.check_task, F.data == "save_task")
async def processing_save_task(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:

    data_task = await state.get_data()
    await state.clear()

    await create_task(session=session, text=data_task.get("text"))

    await callback.answer("Задача сохранена")
    await callback.message.answer(
        text="Готово, для просмотра всех задач отправте команду /tsk."
    )
