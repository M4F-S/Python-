# Module 10 — Functional Programming (FuncMage)

> *"Functions are values; values can be functions."*

Python is not a pure-functional language, but it treats functions as
first-class objects: you can assign them to variables, pass them as
arguments, return them from other functions, and tuck them into lists
and dicts. Add closures, decorators, and `functools`, and you have
enough to write expressive, reusable, testable code.

C calls this "function pointers, plus some sugar." Python makes the
sugar cheap enough that you reach for it every day.

## 1. Lambda expressions

A `lambda` is a one-expression anonymous function. It evaluates to a
function object you can pass wherever a callable is expected.

```python
double = lambda x: x * 2
double(4)                               # -> 8
sorted([{"p": 3}, {"p": 1}], key=lambda d: d["p"])
```

Rules:
- Body is a **single expression**, not a block. No `return`, no
  statements, no `if/elif/else` trees (but `x if cond else y` is fine).
- If the body would need statements, write a `def`.
- PEP 8 discourages `foo = lambda x: ...` — use `def foo(x): ...` for
  named functions. Lambdas shine as *arguments* to `map`/`filter`/
  `sorted(key=...)`.

## 2. Higher-order functions

A function that takes or returns another function.

```python
from collections.abc import Callable


def twice(f: Callable[[int], int]) -> Callable[[int], int]:
    def wrapped(x: int) -> int:
        return f(f(x))
    return wrapped


add1 = lambda x: x + 1
add2 = twice(add1)
add2(5)        # -> 7
```

Import `Callable` from `collections.abc`, not from `typing`; the stdlib
recommendation for Python 3.9+ (and the module's subject line). The
shape `Callable[[Arg1, Arg2, ...], Return]` captures the signature.

### Built-in higher-order tools

- `map(fn, iterable)` — apply `fn` to every item; returns a lazy
  iterator.
- `filter(pred, iterable)` — keep items where `pred(item)` is truthy.
- `sorted(iterable, key=fn)` — stable sort by the value of `fn(item)`.
- `min` / `max` accept a `key=` argument too.
- `sum`, `any`, `all`, `len` — not higher-order, but close cousins.

## 3. Closures and `nonlocal`

A closure is a function plus the enclosing variables it references.
Python builds one automatically whenever an inner function reads or
writes an outer variable:

```python
def counter() -> Callable[[], int]:
    n = 0

    def inc() -> int:
        nonlocal n
        n += 1
        return n

    return inc


c = counter()
c(), c(), c()     # -> 1, 2, 3
```

- `nonlocal` tells Python "this name belongs to the *enclosing function
  scope*, not to a new local." Without it, `n += 1` would raise
  `UnboundLocalError`.
- `global` is forbidden in this module — prefer closures (explicit
  capture) over mutable module-level state.
- Each call to `counter()` creates a brand-new `n`, so two counters are
  fully independent. That's the "two separate counters → independent
  state" rule in Exercise 2.

## 4. `functools` highlights

- `functools.reduce(fn, iterable, initial)` — fold an iterable into a
  single value. Pair with `operator.add`, `operator.mul`, `max`, `min`
  so you never have to re-write `lambda a, b: a + b`.
- `functools.partial(fn, **fixed)` — pre-fill some arguments; returns a
  new callable with a reduced signature. Great for plugging "almost
  there" functions into APIs that demand a specific shape.
- `functools.lru_cache` / `functools.cache` — memoise pure functions.
  `fib.cache_info()` tells you hits vs. misses.
- `functools.wraps(fn)` — copies `__name__`, `__doc__`, `__wrapped__`
  from `fn` onto your wrapper. Always use it inside decorators; without
  it, `help(my_func)` will show the wrapper's blank docstring.
- `functools.singledispatch` — register type-specific implementations of
  a function so dispatch happens on the first argument's runtime type.

Operator module: `operator.add`, `operator.mul`, `operator.itemgetter`,
`operator.attrgetter` — function-object versions of Python's operators,
friendlier to `reduce`/`map` than a lambda.

## 5. Decorators

Syntactic sugar for "replace `fn` with `decorator(fn)`."

```python
import time
from functools import wraps
from collections.abc import Callable
from typing import Any


def spell_timer(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Casting {func.__name__}...")
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"Spell completed in {time.perf_counter() - t0:.3f} seconds")
        return result
    return wrapper


@spell_timer
def fireball() -> str:
    time.sleep(0.1)
    return "Fireball cast!"
```

Parameterised decorators need three nested functions:

```python
def power_validator(min_power: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(power: int, *args, **kwargs):
            if power < min_power:
                return "Insufficient power for this spell"
            return func(power, *args, **kwargs)
        return wrapper
    return decorator


@power_validator(min_power=10)
def cast(power: int, name: str) -> str:
    return f"Successfully cast {name} with {power} power"
```

The outer layer captures the parameter, the middle layer receives the
target function, the inner layer is the actual wrapper.

## 6. `@staticmethod` vs. instance methods

```python
class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        return len(name) >= 3 and all(c.isalpha() or c == " " for c in name)

    def cast_spell(self, name: str, power: int) -> str:
        ...
```

- Instance methods take `self`; they read/write state.
- `@staticmethod` is just a function living inside a class — no `self`,
  no `cls`. Use it when the logic is conceptually part of the class
  but doesn't depend on the instance.
- `@classmethod` (out of scope for this module) takes `cls` and is the
  tool you reach for for alternate constructors.

## When lambdas are the wrong answer

- If the body would span multiple lines.
- If you want to name the function for clarity.
- If you'd unit-test the function in isolation (name it → mypy and
  test reports get better names).

Lambdas are for *one-shot* transformations that are clearer inline than
as a named function three lines away.

## C → Python translations

| C idiom                                              | Python                               |
|------------------------------------------------------|--------------------------------------|
| `int (*cmp)(const void*, const void*)`               | `sorted(items, key=...)`             |
| Callback registered once                             | Closure that captures local state    |
| Hand-written memoisation table                       | `@lru_cache`                         |
| Function-pointer struct table                        | `singledispatch` or dict of callables|
| Macro for logging around a function                  | Decorator with `functools.wraps`     |

Time to open `examples/01_functional_tour.py` for a runnable tour that
exercises every technique in under a hundred lines.
