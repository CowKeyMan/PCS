from dataclasses import dataclass
from omegaconf import OmegaConf
import sys
from pcs.argument_parser import parse_arguments_from_files, parse_arguments_cli
from pcs.pipeline import Pipeline

@dataclass
class A:
    @dataclass
    class B:
        bb: int

    c: int
    d: int
    a: int

    b: B

@dataclass
class B:
    cc: A
    dd: int

c = parse_arguments_cli(A, B)
print(c)

# a = A(*([MISSING] * len(A.__annotations__)))

#
# print(a)

# conf = OmegaConf.structured(A)
# yml = OmegaConf.load("default.yaml")
# print("x" in yml)


# aa = OmegaConf.merge(conf, yml)
# print(type(aa))
# print(aa)
# print(OmegaConf.is_missing(aa, "b"))
# aa.b = A.B(bb=3)
#
# import shlex
# shlex.split
# print(sys.argv)
# # conf = OmegaConf.from_cli()
# # print(conf)

# OmegaConf.from_dotlist(args_list)
c = parse_arguments_from_files(A, B, ["default.yaml"])
c.cc = 3
c.c = 1000
# c.c = 1000

print(c.get_non_null_members_as_dict())
print(c.is_sealed())

c.seal()

c.cc = 4

print(c)
print(c.is_sealed())

def add(c, d):
    return {"dd": c + d}

Pipeline(c, [add]).execute()


print(c)
