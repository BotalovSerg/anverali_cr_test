from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.states import TaskSG
from bot.keyboards.inline_kb import save_task_kb
from bot.database.crud.tasks import create_task, get_all_tasks
from bot.utils import get_tasks_to_string

router = Router()


@router.message(Command("add"))
async def processing_cmd_add(message: Message, state: FSMContext) -> None:
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


@router.callback_query(TaskSG.check_task, F.data == "cansel_task")
async def processing_cansel_task(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.answer("Отмена")
    await callback.message.answer(
        text="Задача не сохранена.\n\n- команда для добавления задачи /add\n- команда для просмотра всех задач /tsk",
    )


@router.callback_query(TaskSG.check_task, F.data == "edit_task")
async def processing_edit_task(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(TaskSG.text)

    await callback.answer("Edit")
    await callback.message.answer(text="Введите задачу заново и отправте сообщение.")


@router.message(Command("tsk"))
async def processing_get_all_tasks(message: Message, session: AsyncSession) -> None:

    list_tasks = await get_all_tasks(session)
    if list_tasks:
        await message.answer(text=get_tasks_to_string(list_tasks))
    else:
        await message.answer(
            text="Список задач пуст.\n\n- команда для добавления задачи /add\n- команда для просмотра всех задач /tsk",
        )
