from enum import EnumMeta
from typing import Any

from pedantic import overrides
from pedantic.decorators.fn_deco_validate.validators import Validator


class IsEnum(Validator):
    def __init__(self, enum: EnumMeta, convert: bool = True) -> None:
        self._enum = enum
        self._convert = convert

    @overrides(Validator)
    def validate(self, value: Any) -> Any:
        try:
            enum_value = self._enum(value)
        except (ValueError, TypeError):
            return self.raise_exception(msg=f'Incorrect value {value} for enum {self._enum}.', value=value)

        if self._convert:
            return enum_value

        return value
