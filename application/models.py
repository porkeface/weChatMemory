# application/models.py
from dataclasses import dataclass

@dataclass
class Contact:
    id: str
    username: str
    nickname: str
    remark: str

@dataclass
class Message:
    id: int
    create_time: int
    talker: str
    content: str
    type: int