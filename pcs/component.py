from typing import Generic, TypeVar

from omegaconf import DictConfig, OmegaConf
from pcs.init import initialize_object_nones

T = TypeVar("T")


class Component(Generic[T]):
    @classmethod
    def init_with_conf(
        cls: "type[Component[T]]", conf: DictConfig, Cls: type[T]
    ) -> "Component[T]":
        runtime = initialize_object_nones(Cls)
        return cls(conf, runtime)

    def __init__(self, conf: DictConfig, runtime: T):
        duplicate_keys = set(conf.keys()).intersection(set(runtime.__dict__))
        assert len(duplicate_keys) == 0, (
            f"Error initializing component - duplicate keys found: {duplicate_keys}"
        )

        super().__setattr__("conf", conf)
        super().__setattr__("runtime", runtime)
        super().__setattr__("sealed", False)

    def seal(self):
        OmegaConf.set_readonly(super().__getattribute__("conf"), True)
        super().__setattr__("sealed", True)

    def is_sealed(self):
        return self.sealed

    def get_conf(self):
        return super().__getattribute__("conf")

    def get_runtime(self):
        return super().__getattribute__("runtime")

    def __getattribute__(self, name):
        if name not in ["conf", "runtime"]:
            return super().__getattribute__(name)
        conf: DictConfig = super().__getattribute__("conf")
        if name in conf.keys():
            if name in conf:
                return getattr(conf, name)
            return None
        runtime: T = super().__getattribute__("runtime")
        if hasattr(runtime, name):
            return getattr(runtime, name)

    def __setattr__(self, name: str, item):
        if name in ["conf", "runtime"]:
            return super().__setattr__(name, item)
        conf: DictConfig = super().__getattribute__("conf")
        if name in conf.keys():
            return setattr(conf, name, item)
        runtime: T = super().__getattribute__("runtime")
        if hasattr(runtime, name):
            return setattr(runtime, name, item)
        raise AttributeError(f"{name} not found in class Component")

    def __hasattr__(self, name):
        return super().__hasattr__(name) or hasattr(self.runtime, name) or hasattr(self.conf, name)

    def __repr__(self):
        conf = super().__getattribute__("conf")
        runtime = super().__getattribute__("runtime")
        sealed = super().__getattribute__("sealed")
        return f"Component({conf=}, {runtime=}, {sealed=})"

    def get_non_null_members_as_dict(self):
        resolved_conf = OmegaConf.to_container(
            super().__getattribute__("conf"), resolve=True
        )
        assert isinstance(resolved_conf, dict)
        result = {k: v for k, v in resolved_conf.items() if v != "???"}
        runtime = super().__getattribute__("runtime")
        result |= {k: v for k, v in runtime.__dict__.items() if v is not None}
        return result
