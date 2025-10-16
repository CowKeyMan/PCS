# from dataclasses import dataclass
#
# from pcs.argument_parser import parse_arguments
# from pcs.component import get_non_null_members_as_dict
# from pcs.init import initialize_object_nones
# from pcs.pipeline import Pipeline
#
#
# @dataclass
# class Component:
#     i: int
#     f: float
#     s: str
#     s2: str
#     result: float
#
#
# def print_add_system(i: int, f: float):
#     print("Add System:", i + f)
#
#
# def result_add_system(i: int, f: float, result: float):
#     return {"result": result + i + f}
#
#
# def print_result(result: float):
#     print("Result:", result)
#
#
# def print_string(s: str):
#     print("s:", s)
#
#
# def print_string2(s2: str):
#     print("s2:", s2)
#
#
# component = initialize_object_nones(Component)
# parse_arguments(component)
#
# pipeline = Pipeline(
#     component,
#     [
#         print_add_system,
#         print_result,
#         result_add_system,
#         print_result,
#         print_string,
#         print_string2,
#     ],
# )
#
# pipeline.execute()
# pipeline.execute()
#
# print(get_non_null_members_as_dict(component))
