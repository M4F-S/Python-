# Module 03 — Data Quest: Python Collections

> **Subject PDF:** `../../py-03.pdf`. Seven exercises, one per collection
> type (list, tuple, set, dict, generator, comprehension) plus a
> command-line warm-up.

> **No file I/O allowed.** All data lives in memory or comes from CLI args.

---

## 1. The four core collections at a glance

| Type | Syntax | Ordered? | Mutable? | Duplicates? | Hashable? |
|---|---|---|---|---|---|
| `list` | `[1, 2, 3]` | yes | yes | yes | no |
| `tuple` | `(1, 2, 3)` | yes | no | yes | yes (if elements are) |
| `set` | `{1, 2, 3}` | no | yes | no | no |
| `dict` | `{"a": 1}` | insertion order (3.7+) | yes | keys unique | no |

"Hashable" means the object can be used as a dict key or set element.
Strings, numbers, and tuples of hashables are hashable; lists and dicts
aren't.

---

## 2. Lists

C arrays with auto-growth, generics, and no bounds checks.

```python
xs: list[int] = [5, 2, 8]
xs.append(1)                 # [5, 2, 8, 1]
xs.insert(0, 99)             # [99, 5, 2, 8, 1]
xs.pop()                     # returns 1, list is now [99, 5, 2, 8]
xs.sort()                    # [2, 5, 8, 99]
sorted(xs, reverse=True)     # [99, 8, 5, 2]  (doesn't mutate xs)
len(xs)                      # 4
2 in xs                      # True  (linear scan — O(n))
xs[1:3]                      # [5, 8]   (slice)
xs[-1]                       # 99  — negative index walks from end
```

### Built-ins you'll want

`len()`, `sum()`, `max()`, `min()` — each work on lists directly.

---

## 3. Tuples

Immutable lists. Great for fixed-shape records (`(x, y, z)`), multi-return
values, and dict keys.

```python
pos: tuple[float, float, float] = (1.0, 2.5, 3.0)
x, y, z = pos              # unpacking
pos[0], pos[-1]            # indexable
pos + (4.0,)               # creates a new 4-tuple (concat)
```

Parens are not what makes a tuple — it's the comma:

```python
just_a_paren = (5)         # -> int
actually_a_tuple = (5,)    # -> (5,)
```

---

## 4. Sets

Hash-based collection of unique elements. `in` is O(1).

```python
achievements = {"Boss Slayer", "First Steps"}
achievements.add("Speed Runner")
achievements.discard("Missing")   # no error if absent
achievements.remove("First Steps")  # raises KeyError if absent
len(achievements)

a = {1, 2, 3}
b = {3, 4, 5}
a | b                 # union:         {1, 2, 3, 4, 5}
a & b                 # intersection:  {3}
a - b                 # difference:    {1, 2}
a ^ b                 # symmetric dif: {1, 2, 4, 5}
# method form: a.union(b), a.intersection(b), a.difference(b)
```

Note: `set()` prints as `set()` (empty), not `{}` — that's a dict.

---

## 5. Dictionaries

Hash map. Keys must be hashable.

```python
inv: dict[str, int] = {"sword": 1, "potion": 5}
inv["shield"] = 2              # insert/update
inv.get("missing", 0)          # safe lookup with default
"sword" in inv                 # O(1) membership
del inv["sword"]
for k, v in inv.items(): ...   # iterate key, value
inv.keys(), inv.values()       # views (lazy)
sum(inv.values())              # works because values are ints
```

---

## 6. Generators and `yield`

A function with `yield` is a **generator**. It doesn't compute everything
up front — it produces values on demand.

```python
def count_up(n: int):
    i = 0
    while i < n:
        yield i
        i += 1

g = count_up(3)
next(g)       # 0
next(g)       # 1
for v in count_up(3): print(v)     # 0, 1, 2
```

Why they matter: you can stream over gigabytes without loading them into
memory. The PDF forces you to use generators for the "endless event
stream" in ex5.

Endless generator:

```python
def gen_event():
    while True:
        yield (random.choice(names), random.choice(actions))
```

Use `next()` in a loop, or a `for ... in` (which Python stops by breaking,
since the generator never ends on its own).

---

## 7. Comprehensions (ex6)

Concise transforms over any iterable.

```python
# list comprehension
squares = [x * x for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]

# dict comprehension
score = {name: random.randint(0, 1000) for name in names}
high = {n: s for n, s in score.items() if s > avg}

# set comprehension
unique = {word.lower() for word in text.split()}
```

The PDF requires one line per comprehension. If it's too long for flake8's
79-char limit, break it inside the brackets.

---

## 8. Command-line args (ex0)

Python uses `sys.argv`:

```python
import sys
print("program name:", sys.argv[0])
print("arguments:", sys.argv[1:])
print("count incl prog:", len(sys.argv))
```

`sys.argv[0]` is the script name (like `argv[0]` in C). The rest are user
arguments as strings. Converting to int requires `int(...)` and is where
`ValueError` comes from.

---

## 9. Exercise map

| # | File | What it teaches |
|---|---|---|
| 0 | `ft_command_quest.py` | `sys.argv`, indexing, `len` |
| 1 | `ft_score_analytics.py` | lists, `sum`/`max`/`min`, filter invalid args |
| 2 | `ft_coordinate_system.py` | tuples, unpacking, `math.sqrt`, validated input loop |
| 3 | `ft_achievement_tracker.py` | sets: union, intersection, difference |
| 4 | `ft_inventory_system.py` | dicts, parsing `item:qty` strings |
| 5 | `ft_data_stream.py` | generators — infinite `gen_event`, consuming `consume_event` |
| 6 | `ft_data_alchemist.py` | list + dict comprehensions, filtering by average |

### Forbidden/authorized notes

- **ex0**: only `sys`, `sys.argv`, `len()`, `print()`.
- **ex1**: add `sum`, `max`, `min`.
- **ex2**: `import math`, `math.sqrt`, `input`, `round`, `print`.
- **ex3**: `import random`, `random.*`, `set(), union, intersection,
  difference`, `len`, `print`. You may NOT use list comprehensions here.
- **ex4**: `sys, sys.argv, len, print, sum, list, round, dict.keys,
  dict.values, dict.update`. No `sorted()`, no comprehensions.
- **ex5**: `next, range, len, print, typing.Generator, random.*`. No list
  comprehensions in the generators.
- **ex6**: `random.*, print, len, sum, round`. **Comprehensions required.**

Read the "Authorized" line every time before you write code. 42's
moulinette scans for forbidden calls.

---

## 10. Type hints

All functions need them (the module requires mypy):

```python
from typing import Generator

def gen_event() -> Generator[tuple[str, str], None, None]:
    while True:
        yield ("alice", "jump")
```

The three `Generator` parameters are `YieldType, SendType, ReturnType`.
For `yield`-only generators, `SendType` and `ReturnType` are `None`.

---

## 11. Testing

```bash
python3 ft_score_analytics.py 1500 2300 1800
python3 ft_score_analytics.py       # no-args path
python3 ft_score_analytics.py abc   # all-invalid path
mypy ft_score_analytics.py
flake8 ft_score_analytics.py
```
