# Proposal: Develop a Dagger Ansible Module

I want to develop a Dagger Ansible Module.

An initial dagger module has already been created in the ./ansible/ directory with the following commands:

- dagger init
- dagger develop --sdk=python

The module should enable the execution of ansible-galaxy commands in an ansible playbook directory.
The directory should be passable as a directory parameter.

The module should also support the following parameters:

- playbook, to execute a specific playbook, type:string
- inventory, to use a specific inventory file, type:string
- extra_vars, to pass additional variables in the form key=value, type: array of strings
- tags, to use specific tags, type: array of strings

## Dagger Module tests

documentation reference: https://docs.dagger.io/reference/best-practices/modules

Implement tests for the Dagger Ansible Module to ensure its functionality and reliability.

Given this example dagger module called `greeter`:

```python
from dagger import function, object_type

@object_type
class Greeter:
    greeting: str = "Hello"

    @function
    def hello(self, name: str) -> str:
        """Greets the provided name"""
        return f"{self.greeting}, {name}!"
```

Creating a test module in the same directory as your main module and writing your tests as Dagger Functions, as shown below:

```bash
mkdir tests
cd tests
dagger init --name=tests --sdk=python --source=.
dagger install ..
```

Then add the following to src/tests/main.py:

```python
@object_type
class Tests:
    @function
    async def hello(self):
        greeting = await dag.greeter().hello("World")

        if greeting != "Hello, World!":
            raise Exception("unexpected greeting")
``

## Testable examples

Implement a example modules, a special modules designed to showcase your own modules, offering better demonstrations

```bash
mkdir -p examples/python
cd examples/python
dagger init --name=examples/python --sdk=python --source=.
dagger install ../..
```

Then add the following to src/examples/main.py:

```python
@object_type
class Examples:
    @function
    async def greeter_hello(self):
        greeting = await dag.greeter().hello("World")
       	# Do something with the greeting
``
