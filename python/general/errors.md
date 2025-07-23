# Error Handling in Python: `try-except` and `raise`

Error handling allows you to control what happens when an error (also called an exception) occurs during program execution. Python provides built-in mechanisms for catching and raising exceptions.

---

## `try-except`: Catching Errors

The `try-except` block is used to catch and handle exceptions. Code that might cause an error is placed inside the `try` block, and the error is caught and handled in the `except` block.

### Syntax:
```python
try:
    # Code that may raise an exception
    risky_code()
except SomeException as e:
    # Code that runs if the exception occurs
    print("An error occurred:", e)
```
### Example:
```python
try:
    number = int(input("Enter a number: "))
    print(10 / number)
except ValueError:
    print("That was not a valid number.")
except ZeroDivisionError:
    print("You cannot divide by zero.")
```
---
## `raise`: Raising Errors Manually
The raise statement allows you to manually trigger an exception when something goes wrong in your program.

### Syntax:
```python
raise ExceptionType("Custom error message")
```
### Example:
```python
def set_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative.")
    print(f"Age is set to {age}")

set_age(-1)
```
## Key Differences Between try-except and raise
| Aspect           | `try-except`                            | `raise`                                  |
| ---------------- | --------------------------------------- | ---------------------------------------- |
| Purpose          | Handles and responds to errors          | Triggers an exception intentionally      |
| Where it is used | Around code that *might fail*           | When you *know something is wrong*       |
| Behavior         | Prevents the program from crashing      | Interrupts normal flow with an exception |
| Typical use case | Handling invalid input, failed file I/O | Validating data, enforcing constraints   |
