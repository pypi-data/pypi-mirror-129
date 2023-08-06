# Hello world

This is an example project demonstrating how to publish a python module to PyPI.

## Installation

Run the following to install:

```bash
$ pip install hello_world
```

## Usage

```python
from helloworld import say_hello

# Generate "Hello, world!"
say_hello()

# Generate "Hello, everybody!"
say_hello("everybody")
```

# Developing Hello world
To install helloworld, along with the tools you need to develop and run tests, run the following in your virtualenv:

```bash
$ pip install -e .[dev]
```