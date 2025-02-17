from aiogram.fsm.state import State, StatesGroup


class TaskSG(StatesGroup):
    text = State()
    check_task = State()
