import inspect
from collections.abc import Mapping
from typing import Callable, TypeAlias

System: TypeAlias = Callable[..., None | Mapping[str, object]]


class Pipeline:
    def __init__(
        self,
        component: object,
        systems: list[System],
        do_null_checks: bool = True,
    ):
        assert len(systems) > 0, "Systems in an empty list"
        self.component: object = component
        self.systems: list[System] = systems
        self.do_null_checks: bool = do_null_checks
        self.current_system: System = systems[0]

    def execute(self) -> None:
        for system in self.systems:
            self.current_system = system
            self.check_for_nulls(system)
            result = system(
                *[
                    getattr(self.component, param_name)
                    for param_name in inspect.signature(system).parameters
                ]
            )
            self.set_component(result)

    def check_for_nulls(self, system: System) -> None:
        if not self.do_null_checks:
            return
        for parameter in inspect.signature(system).parameters:
            assert (
                getattr(self.component, parameter) is not None
            ), f"System: {system.__name__} - Parameter {parameter} was None"

    def set_component(self, result: None | Mapping[str, object]) -> None:
        if result is None:
            return
        for name, obj in result.items():
            setattr(self.component, name, obj)
