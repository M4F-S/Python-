"""Lambdas, closures, functools and decorators in one page."""
import operator
import time
from collections.abc import Callable
from functools import lru_cache, partial, reduce, wraps
from typing import Any


# 1. Lambda + higher-order -------------------------------------------
people = [{"name": "Ada", "age": 36}, {"name": "Bo", "age": 19}]
oldest = max(people, key=lambda p: p["age"])
print("1. oldest ->", oldest["name"])


# 2. Closure ----------------------------------------------------------
def make_accumulator(start: int = 0) -> Callable[[int], int]:
    total = start

    def add(x: int) -> int:
        nonlocal total
        total += x
        return total

    return add


acc = make_accumulator(10)
print("2. closure ->", acc(1), acc(1), acc(1))


# 3. reduce + operator ------------------------------------------------
nums = [1, 2, 3, 4]
print("3. reduce ->", reduce(operator.mul, nums))


# 4. partial ---------------------------------------------------------
def greet(greeting: str, name: str) -> str:
    return f"{greeting}, {name}!"


hello = partial(greet, "Hello")
print("4. partial ->", hello("World"))


# 5. lru_cache -------------------------------------------------------
@lru_cache(maxsize=None)
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)


print("5. fib(30) ->", fib(30), "cache:", fib.cache_info())


# 6. Decorator -------------------------------------------------------
def timed(fn: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(fn)
    def inner(*args: Any, **kw: Any) -> Any:
        t0 = time.perf_counter()
        try:
            return fn(*args, **kw)
        finally:
            print(f"6. {fn.__name__} took {time.perf_counter() - t0:.4f}s")

    return inner


@timed
def slow_add(a: int, b: int) -> int:
    time.sleep(0.05)
    return a + b


print("6. slow_add(2, 3) ->", slow_add(2, 3))
