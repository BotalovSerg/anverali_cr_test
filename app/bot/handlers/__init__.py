from aiogram import Router

from .task_handler import router as router_tasks


def get_routers() -> list[Router]:
    return [
        router_tasks,
    ]
