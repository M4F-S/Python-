# C → Python Translation Appendix

42 cadets typically reach Rank 2 with C as their primary language.
This appendix is a side-by-side cheat sheet for the constructs that
trip people up most when they start using Python. Every Rank 2 course
module assumes the mapping below is in your head; skim this page once
and refer back to it when a Python feature feels like magic.

## Compilation model

| In C                                       | In Python                                   |
|--------------------------------------------|---------------------------------------------|
| `cc main.c -o main` → native binary        | `python3 main.py` runs the source directly  |
| Link objects: `cc a.o b.o -o prog`         | Import modules: `import a, b`               |
| `.h` headers + `.c` sources                | A single `.py` file is both                 |
| Include guards (`#ifndef FOO_H`)           | Automatic — modules cached in `sys.modules` |
| `make` orchestrates compilation            | Usually unnecessary; `pip`/`uv` orchestrate deps |

Python is interpreted. Every module is loaded top-to-bottom once,
then cached. There's no link step, no object files, and no preprocessor.

## Primitive types

```c
int    n = 42;
float  f = 3.14f;
char   c = 'A';
char*  s = "hello";
bool   ok = true;
```

```python
n: int = 42
f: float = 3.14
c: str = "A"      # Python has no 'char' type - strings only
s: str = "hello"
ok: bool = True
```

Python ints are arbitrary precision (no `int`/`long` distinction), its
floats are IEEE-754 doubles, and strings are Unicode.

## Memory management

| In C                                   | In Python                           |
|----------------------------------------|-------------------------------------|
| `malloc` / `free` — manual             | Automatic reference counting + GC   |
| Use-after-free, double-free, leaks     | Largely impossible at the lang level |
| Stack vs. heap explicit                | Nearly everything lives on the heap |
| `struct { int x, y; }` — value type    | Objects are always reference-typed  |

Call `x = list(y)` and you get a *new* list. Call `x = y` and you get
a second binding to the same list; `x.append(1)` mutates what `y`
points to too. That's Python's whole "everything is a reference"
story in one line.

## Arrays and strings

```c
int arr[5] = {1, 2, 3, 4, 5};
int len = sizeof(arr) / sizeof(arr[0]);
for (int i = 0; i < len; i++) printf("%d\n", arr[i]);

char buf[64];
strcpy(buf, "hello ");
strcat(buf, "world");
```

```python
arr = [1, 2, 3, 4, 5]
for n in arr:
    print(n)

# Strings are immutable; concat creates a new string each time.
buf = "hello " + "world"
# Or (cleaner) f-strings for interpolation:
buf = f"hello {name}"
```

Python lists are dynamic arrays; `len(arr)` is O(1). Strings are
immutable, so `s += "x"` creates a fresh string — use `"".join(parts)`
for heavy concatenation.

## Structs and OOP

```c
typedef struct {
    char name[32];
    int  age;
} Person;

Person p = {"Alice", 30};
printf("%s is %d\n", p.name, p.age);
```

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int

p = Person("Alice", 30)
print(f"{p.name} is {p.age}")
```

Real OOP (methods, inheritance) is built in:

```python
class Greeter(Person):
    def hello(self) -> str:
        return f"Hi, I'm {self.name}."
```

## Control flow

```c
for (int i = 0; i < 10; i++) { ... }
while (cond) { ... }
if (a && b) { ... } else if (c) { ... }
switch (x) {
    case 1: ...; break;
    default: ...;
}
```

```python
for i in range(10):
    ...
while cond:
    ...
if a and b:
    ...
elif c:
    ...
match x:
    case 1:
        ...
    case _:
        ...
```

No braces — indentation is the block structure. No semicolons at line
ends. `and` / `or` instead of `&&` / `||`.

## Functions

```c
int square(int x) {
    return x * x;
}
```

```python
def square(x: int) -> int:
    return x * x
```

Python function arguments can be keyword-given
(`square(x=5)`), have defaults (`def f(x=0):`), and accept
variadic `*args, **kwargs`. You don't need to declare every variable's
type, but type hints are required in 42's Rank 2 projects.

## Pointers vs. references

Python has no pointers. Objects pass by *reference*:

```python
def fill(xs: list[int]) -> None:
    xs.append(42)          # mutates the caller's list
```

To get C's "pass-by-value for structs", make a copy:

```python
from copy import deepcopy
fill(deepcopy(original))
```

## Error handling

```c
FILE *f = fopen("foo.txt", "r");
if (f == NULL) {
    perror("fopen");
    return 1;
}
// ...
fclose(f);
```

```python
try:
    with open("foo.txt") as f:      # RAII-style cleanup via `with`
        data = f.read()
except OSError as exc:
    print(f"fopen: {exc}", file=sys.stderr)
    sys.exit(1)
```

No `errno`, no manual `fclose`. Use exceptions for errors, `with`
statements for resources.

## Generic containers

| C pattern                                         | Python                             |
|---------------------------------------------------|------------------------------------|
| Hand-rolled linked list of `Node*`                | `list` / `collections.deque`       |
| Open-addressing hash table                        | `dict`                             |
| Binary-searched sorted array                      | `sorted()` + `bisect`              |
| Unique-set via sorted array                       | `set`                              |
| Tagged union with a discriminator field           | `@dataclass` hierarchy or `match`  |

All four core containers (`list`, `dict`, `set`, `tuple`) are built
into the language and heavily optimised — you almost never roll your
own.

## Function pointers and callbacks

```c
int cmp(const void *a, const void *b) { return *(int*)a - *(int*)b; }
qsort(arr, n, sizeof(int), cmp);
```

```python
arr.sort(key=lambda x: x)            # or key=some_function
arr.sort(key=lambda x: (x.type, x.name))
```

Python's functions are first-class objects: pass them as arguments,
return them, store them in lists and dicts. That's what makes
decorators, callbacks, and strategy patterns so cheap.

## String formatting

```c
char buf[128];
snprintf(buf, sizeof buf, "%s is %d years old", name, age);
```

```python
buf = f"{name} is {age} years old"
# or:
buf = "{} is {} years old".format(name, age)
```

## Build tooling

| C world                                  | Python world                          |
|------------------------------------------|---------------------------------------|
| Makefile with `CC`/`CFLAGS`/`LDFLAGS`    | `pyproject.toml` + `pip`/`uv`/`poetry`|
| `valgrind` for memory leaks              | `tracemalloc` module (rare need)      |
| `gdb` debugger                           | `pdb`, or an IDE debugger             |
| `gprof` / `perf` for profiling           | `cProfile` + `snakeviz`               |
| Static checker (`gcc -Wall -Wextra`)     | `flake8` + `mypy`                     |
| Unit tests via `check` / `criterion`     | `pytest` (used throughout this course)|

## The mental shift that matters most

C makes you think about what the *machine* is doing: registers,
stack frames, pointers, cache lines. Python makes you think about
what the *values* are doing: which objects reference which, what
operations a value supports, how data flows through pipelines.

The 42 Rank 2 projects reward Python thinking:

- Use `list` comprehensions, `dict.get()`, `any()`/`all()`, `sum()`
  instead of hand-rolled loops.
- Lean on exceptions for error paths — no error code `int` returns.
- Let Pydantic validate at the boundary; trust the interior.
- Prefer composing small functions over writing one big one — Python's
  `functools` and closures exist for that.

Revisit this appendix after each module if you catch yourself writing
C-shaped Python. The code will almost always shrink by half.
