from enum import Enum

# ROLE_CHOICES = [
#         ("ADMIN", "ADMIN"),
#         ("MODERATOR", "MODERATOR"),
#         ("LESSEE", "LESSEE"),
#         ("LESSOR", "LESSOR")
#     ]

class RoleType(str, Enum):
    ADMIN = "Администратор"
    MODERATOR = "Модератор сайта"
    LESSEE = "Арендатор"
    LESSOR = "Арендодатель"

    @classmethod
    def choices(cls):
        return [(member.name, member.value) for member in cls]