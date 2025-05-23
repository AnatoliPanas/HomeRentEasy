from enum import Enum


class RoomType(str, Enum):
    SINGLE_ROOM = "Одна комната (студия)"
    ONE_BEDROOM = "Одна комната с отдельной спальней"
    TWO_BEDROOM = "Две комнаты с общей ванной"
    TWO_BEDROOM_ENSUITE = "Две комнаты с отдельными ванными"
    THREE_BEDROOM = "Три комнаты"
    SUITE = "Сьют / Апартаменты"
    SHARED_ROOM = "Общая комната / койко-место"
    PRIVATE_ROOM_IN_SHARED = "Отдельная комната в общей квартире"
    LOFT = "Лофт / Мансарда"
    STUDIO = "Студия"
    HAUS = "Дом"

    @classmethod
    def choices(cls):
        return [(member.name, member.value) for member in cls]