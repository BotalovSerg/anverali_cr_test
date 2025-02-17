from datetime import datetime
import pytz

from bot.database.models import Task

LOCAL_TZ = pytz.timezone("Asia/Yekaterinburg")


def formatted_datetime_to_string(date: datetime) -> str:
    local_datetime = date.astimezone(LOCAL_TZ)
    return local_datetime.strftime("%A, %d %B · %H:%M")


def get_tasks_to_string(data_list: list[Task]) -> str:
    result = ""
    for item in data_list:
        formatted_date = formatted_datetime_to_string(item.time_create)
        string = f"#{item.id}. Text: {item.text} \nTime create: {formatted_date}\n\n"
        result += string

    return result
