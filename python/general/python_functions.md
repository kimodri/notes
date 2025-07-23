# Arbitrary Arguments

**We need to think about the data type of the arguments we need for a function so are the number of arguments.**

- Arbitrary Argumentts: allow functions to accept any number of arguments

## *args
To do that we place `*` in front of a single argument `args`:
```python
def introduction(name, *args):
    """This function is used to introduce myself."""

    print(f"Hello my name is {name}")
    for skill in args:
        print(f" - {skill}")

introduction("Kim", "Python", "Flask", "Pandas")
```

Inside the `args` is `('Python', 'Flask', 'Pandas')` so `args` is like an unnamed tuple.

> Why we put `*` before `args` when `*` is for unpacking?

**Actually,** 

| Context                                          | Role of `*`                   | What it means                                |
| ------------------------------------------------ | ----------------------------- | -------------------------------------------- |
| When **defining** a function (`def func(*args)`) | **Pack** positional arguments | Pack any number of values into a tuple       |
| When **calling** a function (`func(*args)`)      | **Unpack** a sequence         | Unpack the tuple/list into individual values |


## **kwargs

- This allows a python function to accept any number of keyword arguments
- `kwargs` act as a dictionary

```python

def print_profile(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_profile(name="Kim", age=15, role="Student")

```

The same goes here when using `**`, when defining a function, it acts as a packer of the keyword arguments someone passed, where as when you use it when calling a function it unpacks your dictionary:

```python
names = ["Audrey", "Kim"]
greet_all(*names)

profile = {"name": "Audrey", "role": "Student"}
print_profile(**profile)
```