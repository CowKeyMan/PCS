# Pipeline Component System (PCS)

TODO
<!---->
<!-- A strange programming framework -->
<!---->
<!-- The name is inspired by Entity Component System (ECS) -->
<!---->
<!-- ## Why? -->
<!---->
<!-- Why create this? I often find myself not liking the programs I create, and then end up rewriting them to be better, but they still end up quite brittle. This is a programming framework to make code cleaner and hopefully more maintainable. Have I succeeded in my goal? I'm not sure, but I will try it out myself more and update this documentation here if it is good or not. -->
<!---->
<!-- ## Introduction -->
<!---->
<!-- I will first discuss the few simple components which make up this framework, then connect them together, explaining choices I took along the way. If you wish to see an example of how this all ties together, look at `examples/basic.py`. -->
<!---->
<!-- ### Component -->
<!---->
<!-- Think of the component as your global database. Each piece of persistent data (literal or object) is stored here. It is a dataclass, and it is the only dataclass (unless you want to nest them ofcourse). The reason for this design choice is that this way, we ALWAYS know where the data is. We do not have to guess which class owns what. The Component owns everything. A simple component looks like the following: -->
<!---->
<!-- ```python -->
<!-- @dataclass -->
<!-- class Component:  # Note: the name is not important. I like to use `Data` as well -->
<!--     i: int -->
<!--     f: float -->
<!--     s: str -->
<!--     result: float -->
<!---->
<!-- component = Component(1, 2, 'hello', -1) -->
<!-- ``` -->
<!---->
<!-- Components can store anything. Note: the types are recommended (for static analysers) but not enforced. -->
<!---->
<!-- ### Systems -->
<!---->
<!-- Systems are functions, with parameter names equivalent to the fields in the component. That's it. An example system may look like the following: -->
<!---->
<!-- ```python -->
<!-- def print_add_system(i: int, f: float):  # Note: the variable names match those in the component exactly -->
<!--     print("Add System:", i + f) -->
<!---->
<!---->
<!-- def result_add_system(i: int, f: float, result: float): -->
<!--     result = result + i + f -->
<!--     return {"result": result} -->
<!---->
<!---->
<!-- def result_add_system2(i: int, f: float, result: float): -->
<!--     return {"result": result + i + f}  # Note: the key matches the variable names in the component exactly -->
<!-- ``` -->
<!---->
<!-- Take note of the return at the end of the last 2 systems. We will discuss this syntax in the `Pipeline` section. -->
<!---->
<!-- ### Pipeline -->
<!---->
<!-- A pipeline takes a component, and a list of systems, then automatically passes the fields of the component to the systems, and writes results back to the component. -->
<!---->
<!-- An example pipeline looks like this: -->
<!---->
<!-- ```python -->
<!-- component = Component(1, 2, 'hello', -1) -->
<!-- pipeline = Pipeline( -->
<!--     component, [print_add_system, result_add_system, result_add_system2] -->
<!-- ) -->
<!-- pipeline.execute() -->
<!-- pipeline.execute()  # Execute pipeline a second time -->
<!-- ``` -->
<!---->
<!-- When a system returns a dictionary, the keys of the dict are interpreted to be the names of the component variables to replace with the value of the respective key. So the final 2 systems in the Systems examples will replace the `result` field. -->
<!---->
<!-- Note that this helps us avoid having to pass parameters around, as it is done automatically for us, which cleans up the code base tremendously, as we have a concise pipeline definition, and when we call `Pipeline.execute`, we execute the 3 functions. -->
<!---->
<!-- ### Other handy tools -->
<!---->
<!-- #### `initialize_object_nones` -->
<!---->
<!-- If we want to initialize all the component variables to `None`, instead of: -->
<!---->
<!-- ```python -->
<!-- component = Component(None, None, None, None) -->
<!-- ``` -->
<!---->
<!-- We can do: -->
<!---->
<!-- ```python -->
<!-- from pcs.init import initialize_object_nones -->
<!---->
<!-- component = initialize_object_nones(Component) -->
<!-- ``` -->
<!---->
<!-- Why would we want to do this? Well sometimes we want to initialize only some of our variables in the Component object, but not all. So we initialize everything initially to `None`s, and then replace the `None`s with the actual value we want. Look at the `parse_arguments` section to find out a more useful reason for this! -->
<!---->
<!-- #### `parse_arguments` -->
<!---->
<!-- This function is here to replace all your argument parsing forever! By specifying default variables for some of your arguments in a yaml file, these will be loaded into your component. All you need to do is call: -->
<!---->
<!-- ```python -->
<!-- from pcs.init import initialize_object_nones -->
<!-- from pcs.argument_parser import parse_arguments -->
<!---->
<!-- component = initialize_object_nones(Component) -->
<!-- parse_arguments(component) -->
<!-- ``` -->
<!---->
<!-- An example of such a yaml file is in `examples/configs/default.yaml` -->
<!---->
<!-- Then to run your application, you can call (for the example): `python examples/basic.py --args-files=examples/configs/default.yaml,examples/configs/override1.yaml --rest s="hello world" -r s2="hello world2"` -->
<!---->
<!-- Note: config files specified later will override earlier ones, and 'rest' options will override options in the config files. You can also use `-r` as a shorthand for `--rest`. -->
<!---->
<!-- You will need to call `initialize_object_nones` beforehand. -->
<!---->
<!-- ## Some pattern ideas -->
<!---->
<!-- * Use `parse_arguments` on a different component than your main component, and maybe pass the 'args' component to the main component. -->
<!-- * Nested pipelines -->
