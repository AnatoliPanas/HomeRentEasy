from enum import Enum


class WaitingStatus(str, Enum):
    PENDING = 'В ожидании'
    CONFIRMED = 'Подтверждено'
    CANCELLED = 'Отменено'
    DECLINED = 'Отклонено'

    @classmethod
    def choices(cls):
        return [(member.name, member.value) for member in cls]