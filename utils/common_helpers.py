import re

from loader import Locale

def generate_link_to_msg(chat_id: int, msg_id: int) -> str:
    shift = -1_000_000_000_000
    return f"https://t.me/c/{shift - chat_id}/{msg_id}"


def get_id_from_view_text(message: str) -> int:
    try:
        return re.findall(pattern=Locale.Task.ID + r":\s(\\d+)", string=message)[0]
    except KeyError:
        raise KeyError  # !TODO raise normal exception
