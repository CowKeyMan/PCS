from dataclasses import dataclass
from pcs.init import initialize_object_nones
from pcs.argument_parser import parse_arguments
from pcs.pipeline import Pipeline


@dataclass
class Component:
    i: int
    f: float
    s: str
    result: float


def print_add_system(i: int, f: float):
    print("Add System:", i + f)


def result_add_system(i: int, f: float, result: float) -> dict[str, float]:
    return {"result": result + i + f}


def print_result(result: float):
    print("Result:", result)


component = initialize_object_nones(Component)
parse_arguments(component)

pipeline = Pipeline(
    component, [print_add_system, print_result, result_add_system, print_result]
)

pipeline.execute()
pipeline.execute()
