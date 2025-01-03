from typing import Any

from sqlalchemy import Integer, TypeDecorator


class IntEnum(TypeDecorator):
    """
    Enables passing in a Python enum and storing the enum's *value* in the db.
    The default would have stored the enum's *name* (ie the string).
    """

    impl = Integer
    _enum_type: Any

    def __init__(self, *args, **kwargs):
        super(IntEnum, self).__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if isinstance(value, int):
            return value

        return value.value

    def process_result_value(self, value, dialect):
        return self._enum_type(value)
