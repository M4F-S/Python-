# Module 05 — Polymorphism (Code Nexus)

> *"One interface, many implementations."*
>
> The Code Nexus project stitches together the OOP patterns from Modules 01–04 to
> build a data-processing pipeline that can cope with any data type you throw at
> it. The trick is *polymorphism*: the caller never cares which concrete class is
> on the other end of the reference, only that the **shape** of the object
> matches what it needs.

## Why you care (C → Python map)

| C idiom                                      | Python equivalent                          |
|----------------------------------------------|--------------------------------------------|
| `struct Base { void (*fn)(void*); }` vtable  | A class with an `@abstractmethod`          |
| Function pointer field set per-instance      | Overridden method on a subclass            |
| `void *` + tagged union                      | Duck typing / `typing.Protocol`            |
| `qsort`'s `int (*cmp)(const void*, ...)`     | Passing any object with a `.compare()` method |

Polymorphism in C is "DIY vtables": you fill in function pointers manually and
cast `void*` in and out. In Python, the runtime does the dispatch for you — the
attribute lookup rule walks the MRO (Method Resolution Order) of the object's
class, so calling `processor.ingest(data)` picks the right overridden method
automatically.

## The three flavours of polymorphism in Python

### 1. Inheritance + method overriding (classical)

```python
class Shape:
    def area(self) -> float:
        raise NotImplementedError

class Circle(Shape):
    def __init__(self, r: float) -> None:
        self.r = r
    def area(self) -> float:
        return 3.14159 * self.r ** 2

def total(shapes: list[Shape]) -> float:
    return sum(s.area() for s in shapes)  # no `if isinstance(...)` needed
```

The caller passes a `list[Shape]`, but each `s.area()` dispatches to the
*actual* class of `s`. That's runtime polymorphism.

### 2. Abstract Base Classes (ABC)

`raise NotImplementedError` is a weak contract — nothing stops you from
instantiating `Shape` itself. ABCs enforce the contract:

```python
import abc

class Shape(abc.ABC):
    @abc.abstractmethod
    def area(self) -> float: ...

Shape()  # TypeError: Can't instantiate abstract class Shape
```

Key points:
- Inherit from `abc.ABC`.
- Mark required methods with `@abc.abstractmethod`.
- A subclass that leaves any abstract method unimplemented is itself abstract
  and cannot be instantiated.
- Concrete (non-abstract) methods can still live on the base class — they are
  shared by every subclass.

### 3. Duck typing / `typing.Protocol` (structural subtyping)

Sometimes you don't *want* a common base class. You just want "anything with
this method." That's what `Protocol` is for:

```python
import typing

class SupportsClose(typing.Protocol):
    def close(self) -> None: ...

def shutdown(x: SupportsClose) -> None:
    x.close()
```

`shutdown()` accepts any object that has `close()` — no inheritance required.
`mypy` still checks the shape at compile time.

> Use ABC when you own the hierarchy and want to share code. Use Protocol when
> you want to accept *plugins* from the outside world (like export plugins in
> Exercise 2).

## Method overriding vs. overloading

Python has no function overloading like C++. There is one `def` per name; the
last one wins. To support multiple signatures you either:

1. Widen the parameter type (`int | float | list[int | float]`), **or**
2. Use `@typing.overload` to declare multiple type signatures for the type
   checker while providing a single runtime implementation.

In this module you'll use option (1) to let each specialized ingest method
express which types it accepts, while the base class stays generic with
`Any`.

## LSP — Liskov's substitution principle

If code expects a `DataProcessor` and you hand it a `NumericProcessor`, the
program must still work correctly. Practical consequences:

- Don't make overridden methods require *more* than the base did (no stricter
  preconditions).
- Don't make them return *less* than the base did (no weaker postconditions).
- `validate(self, data: Any)` keeps the same signature in every subclass —
  each one just narrows the concept of "valid" for its own data type.

## Internal storage pattern used by exercises

`DataProcessor` subclasses buffer ingested values and emit them oldest-first
via `output() -> tuple[int, str]`. The `int` is a processing **rank** — a
monotonically increasing counter — and the `str` is the ingested data
serialized to text. A deque-style list works:

```python
self._buffer: list[str] = []
self._rank: int = 0       # next rank to assign
```

Reading `output()` pops index 0 and returns `(rank, value)`.

## Summary of what you'll build

- **ex0** — `DataProcessor(ABC)` with `NumericProcessor`, `TextProcessor`,
  `LogProcessor`. Abstract `validate`/`ingest`, concrete `output`.
- **ex1** — `DataStream` that registers processors and routes each element in
  a stream to whichever processor can validate it.
- **ex2** — `ExportPlugin(Protocol)` with CSV and JSON plugins, and
  `output_pipeline()` that drains processors through a plugin.

Open `examples/01_polymorphism_tour.py` for a runnable tour before starting
the exercises.
