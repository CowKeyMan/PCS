import inspect
from collections.abc import Mapping
from typing import Callable, TypeAlias

from pcs.component import Component

System: TypeAlias = Callable[..., None | Mapping[str, object]]


class Pipeline:
    def __init__(
        self,
        component: Component,
        systems: list[System],
        do_null_checks: bool = True,
        do_seal_check: bool = True,
    ):
        assert len(systems) > 0, "Systems in an empty list"
        if do_seal_check:
            assert component.is_sealed(), "You need to call seal on the component object to make the config objects static, or otherwise set `do_seal_check` to false for this pipeline"
        self.component = component
        self.systems = systems
        self.do_null_checks = do_null_checks
        self.current_system = systems[0]

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
