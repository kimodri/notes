# Python Modules & Packages: Functions Only

## What is a module?

A module is any `.py` file that contains Python code — usually functions or variables.

```python
# math_utils.py

def add(a, b):
    return a + b
```
# What is a package?
A package is a folder with a special file called `__init__.py`.

This tells Python: "Treat this folder as a package that can be imported."

Example folder structure:

my_project/\
├── main.py\
└── tools/\
&emsp;&ensp;    ├── __init__.py\
&emsp;&ensp;      ├── math_utils.py     # add(), subtract()\
&emsp;&ensp;      └── string_utils.py   # clean_text()\

# What does __init__.py do?
It controls what is exposed at the package level — meaning what you can import like this:

```python
from tools import add
```

If you want that to work, you must write in `__init__.py`:

```python
from .math_utils import add
```

Otherwise, you’d have to import like this:
```python
from tools.math_utils import add
```

# So... why use `__init__.py` at all?
Because it gives control over what the outside world sees and uses.

- Anything not in `__init__.py` is still accessible by going deeper (e.g. tools.math_utils.subtract)
- But if it’s not in `__init__.py`, it cannot be accessed directly from the folder/package name (e.g. from tools import subtract)

| Written in `__init__.py`? | How to import                           | How to use in `main.py`          | Implication                                                 |
| ------------------------- | --------------------------------------- | -------------------------------- | ----------------------------------------------------------- |
| Yes                       | `from tools import add`                 | `add(2, 3)`                      | Exposed at top level, easy to use                           |
| No                        | `from tools.math_utils import subtract` | `subtract(4, 1)`                 | Still usable, but not part of the official public interface |
