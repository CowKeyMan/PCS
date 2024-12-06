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
        do_type_checks: bool = True,
    ):
        assert len(systems) > 0, "Systems in an empty list"
        self.component: object = component
        self.systems: list[System] = systems
        self.do_null_checks: bool = do_null_checks
        self.do_type_checks: bool = do_type_checks
        self.current_system: System = systems[0]

    def execute(self) -> None:
        for system in self.systems:
            self.current_system = system
            self.check_for_nulls(system)
            self.check_for_types(system)
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

    def check_for_types(self, system: System) -> None:
        if not self.do_type_checks:
            return
        parameters = inspect.signature(system).parameters
        for param in parameters:
            self.assert_type_annotation(
                self.component.__annotations__[param],  # pyright: ignore[reportAny]
                parameters[param].annotation,  # pyright: ignore[reportAny]
                f"System {system.__name__} - Input {param} has wrong type",
            )

    def set_component(self, result: None | Mapping[str, object]) -> None:
        if result is None:
            return
        assert isinstance(result, dict), (
            f"System {self.current_system.__name__} - "
            f"Result is not None or a dictionary"
        )
        for name, obj in result.items():
            self.assert_type_obj(
                self.component.__annotations__[name],  # pyright: ignore[reportAny]
                obj,
                (
                    f"System {self.current_system.__name__} "
                    f"- Output {name} has wrong type"
                ),
            )
            setattr(self.component, name, obj)

    @staticmethod
    def assert_type_obj(parent_annotation: type, obj: object, message: str) -> None:
        parent_origin = getattr(parent_annotation, "__origin__", parent_annotation)
        assert (type(obj) is parent_annotation) or isinstance(
            obj, parent_origin
        ), message

    @staticmethod
    def assert_type_annotation(
        parent_annotation: TypeAlias, child_annotation: TypeAlias, message: str
    ) -> None:
        child_origin = getattr(child_annotation, "__origin__", child_annotation)
        parent_origin = getattr(parent_annotation, "__origin__", parent_annotation)
        assert isinstance(parent_origin, type) or parent_origin is TypeAlias
        assert (child_annotation == parent_annotation) or isinstance(
            child_origin, parent_origin
        ), message
