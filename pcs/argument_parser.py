import oyaml as yaml
import argparse


class Args(argparse.Namespace):
    def __init__(self):
        super().__init__()
        self.args_files: str = ""
        self.rest: list[str] = []


def parse_arguments(obj: object) -> None:
    args = do_parse_arguments()
    update_dict = get_update_dict_from_comma_separated_file_list(args.args_files)
    update_dict_with_rest_arguments(update_dict, args.rest)
    update_object(obj, update_dict)


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
        nargs="+",
        help=(
            "Set a number of key-value pairs like <key>=<value>. "
            "Values may have spaces if the whole value is wrapped"
            'in quotes such as <key>="this is a value". These arguments'
            "take precedence over those that come from files"
        ),
    )
    args = Args()
    args = parser.parse_args(namespace=args)
    return args


def get_update_dict_from_comma_separated_file_list(files: str) -> dict[str, object]:
    return get_update_dict_from_files(files.split(","))


def get_update_dict_from_files(files: list[str]) -> dict[str, object]:
    if len(files) == 1 and files[0] == "":
        return {}
    args: dict[str, object] = {}
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            args |= yaml.safe_load(f)
    return args


def update_dict_with_rest_arguments(
    update_dict: dict[str, object], rest: list[str]
) -> None:
    for r in rest:
        key, value = r.split("=")
        if value.isdigit():
            value = int(value)
        else:
            try:
                value = float(value)
            except ValueError:
                pass  # not an int nor a float
        update_dict[key] = value


def update_object(obj: object, update_dict: dict[str, object]) -> None:
    for key, value in update_dict.items():
        assert hasattr(obj, key), f"obj has no attribute {key}"
        setattr(obj, key, value)
