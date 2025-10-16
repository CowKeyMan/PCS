import argparse
from typing import TypeVar

from omegaconf import DictConfig, OmegaConf

from pcs.component import Component

T = TypeVar("T")


def parse_arguments_cli(ClsConf: object, ClsRealtime: type[T]) -> Component[T]:
    conf = OmegaConf.structured(ClsConf)
    args = do_parse_arguments()
    conf = update_dict_with_comma_separated_file_list(conf, args.args_files)
    assert isinstance(conf, DictConfig)
    conf = update_dict_with_rest_arguments(conf, args.rest)
    assert isinstance(conf, DictConfig)
    return Component.init_with_conf(conf, ClsRealtime)


def parse_arguments_from_files(
    ClsConf: object, ClsRealtime: type[T], files: list[str]
) -> Component[T]:
    conf = OmegaConf.structured(ClsConf)
    conf = update_dict_with_files(conf, files)
    assert isinstance(conf, DictConfig)
    return Component.init_with_conf(conf, ClsRealtime)


class Args(argparse.Namespace):
    def __init__(self):
        super().__init__()
        self.args_files: str = ""
        self.rest: list[str] = []


def do_parse_arguments() -> Args:
    parser = argparse.ArgumentParser()
    _ = parser.add_argument(
        "--args-files",
        "-f",
        required=False,
        help=(
            "A list of comma separated yaml files, where the keys in the "
            "latest files will overwrite those in previous files"
        ),
    )
    _ = parser.add_argument(
        "--rest",
        "-r",
        action="append",
        help=(
            "Set a number of key-value pairs like <key>=<value>. "
            "Values may have spaces if the whole value is wrapped"
            'in quotes such as <key>="this is a value". These arguments'
            "take precedence over those that come from files"
        ),
    )
    args = parser.parse_args(namespace=Args())
    return args


def update_dict_with_comma_separated_file_list(conf: DictConfig, files: str):
    return update_dict_with_files(
        conf, files.split(",") if len(files) > 0 else []
    )


def update_dict_with_files(conf: DictConfig, files: list[str]):
    return OmegaConf.merge(conf, *[OmegaConf.load(f) for f in files])


def update_dict_with_rest_arguments(conf: DictConfig, rest: list[str]):
    return OmegaConf.merge(conf, OmegaConf.from_dotlist(rest))
