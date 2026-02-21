"""
An example showing pcs in action. After installing the library `pip install pipeline-component-system`, you can navigate to the examples directory and run `python example.py --args-files=configs/default.yaml,configs/override1.yaml -r a4=400 -r b.b2=200 -r b.b2=500`
"""

import multiprocessing
from dataclasses import dataclass

import omegaconf

from pcs.argument_parser import parse_arguments_cli
from pcs.pipeline import Pipeline


@dataclass
class B:
    b1: int
    b2: int
    b3: int
    b4: int
    b5: int
    b6: int


@dataclass
class A:
    a1: int
    a2: int
    a3: int
    a4: int
    a5: int
    b: B
    reference: int


@dataclass
class C:
    c1: int
    c2: int
    c3: int
    c_complex: (
        multiprocessing.SimpleQueue
    )  # We can have more than simple types in runtime classes


# Look at the implementation of this function in argmument_parser.py for the exact details, and if you want to do argument parsing outside of the CLI
data = parse_arguments_cli(A, C)  # A are constants, C are runtime variables

assert (
    str(data)
    == "Component(conf={'a1': 1, 'a2': -2, 'a3': -3, 'a4': 400, 'a5': '???', 'b': {'b1': 1, 'b2': 500, 'b3': -3, 'b4': -4, 'b5': '???', 'b6': '???'}, 'reference': '${a1}'}, runtime=C(c1=None, c2=None, c3=None, c_complex=None), sealed=False)"
), f"Actual: {str(data)}"

assert (
    str(data.get_conf())
    == "{'a1': 1, 'a2': -2, 'a3': -3, 'a4': 400, 'a5': '???', 'b': {'b1': 1, 'b2': 500, 'b3': -3, 'b4': -4, 'b5': '???', 'b6': '???'}, 'reference': '${a1}'}"
), f"Actual: {str(data.get_conf())}"

assert (
    str(data.get_conf(resolve=True))
    == "{'a1': 1, 'a2': -2, 'a3': -3, 'a4': 400, 'a5': '???', 'b': {'b1': 1, 'b2': 500, 'b3': -3, 'b4': -4, 'b5': '???', 'b6': '???'}, 'reference': 1}"
), f"Actual: {str(data.get_conf(resolve=True))}"

data.a5 = -500

data.seal()  # Now we can no longer edit 'data.a'

# Asserting that read only works as expected
try:
    data.a5 = -5000000
except omegaconf.ReadonlyConfigError:
    assert data.a5 == -500


def add(x: int, y: int):
    return x + y


def store_a_into_c(a1: int, a2: int):  # Use type hinting here
    return {"c1": a1, "c2": a2}


def add_a2_and_c2_and_store_into_c2(c2: int, a2: int):
    return {"c2": add(c2, a2)}


init_pipeline = Pipeline(
    component=data,
    systems=[store_a_into_c],
    do_null_checks=True,  # Set when you want to allow passing null values as parameters to your system. To be avoided, since in my opnion null checks are to be avoided.
    do_seal_check=True,  # Set to false when you still want to edit the constant parts of the component. Recommended if you have a system which need to do some 'post-init' operations on the constants (ex: computing and caching some values which later on should be transformed into read-only). Should be avoid in other cases
)
add_pipeline = Pipeline(
    component=data,
    systems=[lambda b, c1: {"c1": c1 + b.b1}, add_a2_and_c2_and_store_into_c2],
    # By default both do_null_checks and do_seal_check are True
)

init_pipeline.execute()
assert data.c1 == data.a1 and data.c2 == data.a2
assert data.c1 == 1 and data.c2 == -2
add_pipeline.execute()
assert data.c1 == 2  # We added b1 to this, which is 1
assert data.c2 == -4  # We added a2 to this, which is -2
add_pipeline.execute()  # We can run pipelines as many times as we want
assert data.c1 == 3 and data.c2 == -6

assert (
    str(data)
    == "Component(conf={'a1': 1, 'a2': -2, 'a3': -3, 'a4': 400, 'a5': -500, 'b': {'b1': 1, 'b2': 500, 'b3': -3, 'b4': -4, 'b5': '???', 'b6': '???'}, 'reference': '${a1}'}, runtime=C(c1=3, c2=-6, c3=None, c_complex=None), sealed=True)"
)
