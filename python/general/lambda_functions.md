# Lambda Functions

Take this function:
```python
def average(values):
    average_value = sum(value) / len(values)
    return average_value
```
There is a quicker way to achieve this function, comes `lambda` functions
- It is an anonymous function
- Syntax when *defining*: `lambda argument(s): expression`
    - `x` acts as an argument
    - `expression` is the body
- Syntax when *calling*: `(lambda x: expression)(argument)`

```python
lambda x: sum(x) / len(x)
```

**Assigning lambda to a variable:**
- Since we know that all functions are just objects, we can assign it to a variable
```python
average = lambda x: sum(x) / len(x)

average([3, 6, 9])
```

**Lambda with more than 1 argument:**
```python
(lambda x, y: x**y)(2, 3)
```

**Lambda with iterables:**
- If we want to work on iterables with lambdas we often use `map()`
- `map()` applies a function to all elements in an iterable
```python
names = ['Kim', 'Audrey', 'Magan']
capitalize = map(lambda x: x.capitalize(), names)
print(list(capitalize))
```
