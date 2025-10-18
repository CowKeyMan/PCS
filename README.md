# Pipeline Component System (PCS)

TODO

A strange programming framework

The name is inspired by Entity Component System (ECS)

## Why?

Why create this? I often find myself not liking the programs I create, and then end up rewriting them to be better, but they still end up quite brittle. This is a programming framework to make code cleaner and hopefully more maintainable. Have I succeeded in my goal? I have been using this framework for some time now and it has definitely helped my development speed and mental fatigue a lot! So yes, it has helped me achieve my goal!

## Introduction

I will first discuss the few simple components which make up this framework, then connect them together, explaining choices I took along the way. If you wish to see an example of how this all ties together, look at `examples/example.py`.

### Component

Think of the component as your global database. Each piece of persistent data (literal or object) is stored here. It is a dataclass, and it is the only dataclass (unless you want to nest them ofcourse). The reason for this design choice is that this way, we ALWAYS know where the data is. We do not have to guess which class owns what, like in those OOP messes.

The Component distinguishes between 2 data types: config (constant / defined at the start then not changed after initialization) and runtime (dynamic data which changes during runtime). The config variables can only be of primitive types (a restriction which comes from omegaconf, which this project depends on). Whereas the config class is

```python
@dataclass
class Config:  # Note: the name is not important
    i: int  # Only primitive types in the config class
    f: float
    s: str
    result: float

@dataclass
class Dynamic:
    di: int  # Dynamic class can also take complex types

data = parse_arguments_cli(Config, Dynamic)

print(data.i)  # Print's the Config class' 'i'
print(data.di)  # Print's the Runtime class' 'i'
```

We can print this data object and we can also serialize it with pickle. The types are necessary for the Config dataclass, and recommended for the Dynamic class. They are enfored in the Config class, but not the Dynamic.

### Systems

Systems are functions, with parameter names equivalent to the fields in the component. That's it. An example system may look like the following:

```python
def print_add_system(i: int, f: float):  # Note: the variable names match those in the component exactly
    print("Add System:", i + f)


def result_add_system(i: int, f: float, result: float):
    result = result + i + f
    return {"result": result}


def result_add_system2(i: int, f: float, result: float):
    return {"result": result + i + f}  # Note: the key matches the variable names in the component exactly
```

Take note of the return at the end of the last 2 systems. We will discuss this syntax in the `Pipeline` section.

### Pipeline

A pipeline takes a component, and a list of systems, then automatically passes the fields of the component to the systems, and writes results back to the component.

An example pipeline looks like this:

```python
component = Component(1, 2, 'hello', -1)
pipeline = Pipeline(
    component, [print_add_system, result_add_system, result_add_system2]
)
pipeline.execute()
pipeline.execute()  # Execute pipeline a second time
```

When a system returns a dictionary, the keys of the dict are interpreted to be the names of the component variables to replace with the value of the respective key. So the final 2 systems in the Systems examples will replace the `result` field.

Note that this helps us avoid having to pass parameters around, as it is done automatically for us, which cleans up the code base tremendously, as we have a concise pipeline definition, and when we call `Pipeline.execute`, we execute the 3 functions.

### Other handy tools

`parse_arguments_cli` will read your argvs using argparse and give you a component object ready to use. So you may run your file like so: `file.py --args-files="file1.yaml,file2.yaml" --rest a=1 --rest b=2`. Consecutive files will overwrite the previous entries, and `--rest` take precendence always, but each `--rest` takes precedence over the previous.

* `--args-files` can be shortened to `-f`
* `--rest` can be shortened to `-r`

## Some pattern ideas

* Nested pipelines
