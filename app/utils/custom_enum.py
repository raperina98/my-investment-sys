from enum import Enum


class CustomEnum(Enum):
    def __str__(self):
        return str(self.value)
