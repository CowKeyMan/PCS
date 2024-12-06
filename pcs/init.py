from typing import TypeVar

T = TypeVar('T')

def initialize_object_nones(Cls: type[T]) -> T:
    return Cls(*([None] * len(Cls.__annotations__)))
