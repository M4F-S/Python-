# Module 00 — Growing Code: Python Fundamentals

> **Subject PDF:** `../../py-00.pdf` — read it first. This lesson expands on it.
> **Goal:** Python syntax, variables, `if`/`else`, loops, functions, `input`/`print`,
> and type hints — all applied to 8 garden-themed exercises.

---

## 1. C vs Python in 60 seconds

| C | Python |
|---|---|
| `int x = 5;` | `x = 5` |
| `#include <stdio.h>` | `import sys` (if needed) |
| `printf("%d\n", x);` | `print(x)` |
| `scanf("%d", &x);` | `x = int(input())` |
| Braces `{ }` define blocks | **Indentation** defines blocks (4 spaces, same depth) |
| Declare types up front | Types are attached to values, not variables (duck typing) |
| Semicolons end statements | Newlines end statements (no `;`) |
| `int main(void) { ... }` | You write functions; there is no main for this module |
| Pointers, `malloc`, `free` | No manual memory — objects are garbage-collected |
| `==` only compares value for primitives | `==` compares value; `is` compares identity (like pointer equality) |
| `true` / `false` | `True` / `False` (capital!) — `0`, `""`, `[]`, `None` are falsy |
| No booleans pre-C99 | `bool` is a real type, subclass of `int` |

### Indentation matters

```python
if x > 0:
    print("positive")    # 4 spaces — this is inside the if
    print("still inside")
print("always runs")     # outside the if
```

Mixing tabs and spaces breaks everything. Pick 4 spaces (PEP 8) and stick to
it. Your editor should insert 4 spaces when you press Tab.

### No declarations

```python
name = "tomato"   # str
count = 42        # int
count = "forty"   # fine — Python re-binds the name to a new string
```

The variable itself has no type. The **object** it points to does. Think of
Python names as labels you stick onto objects, and rebinding moves the label.

---

## 2. The eight pillars you need for Module 00

### 2.1 `print()`

```python
print("hello")                     # hello
print("x =", 5)                    # x = 5 (auto-spaces between args)
print("a", "b", sep="-", end="!")  # a-b!
```

### 2.2 `input()`

Always returns a **string** — never a number, even if the user types `42`.

```python
s = input("Enter name: ")      # prompt printed, waits for Enter, returns str
n = int(input("Enter n: "))    # wrap with int() to parse a number
```

For Module 00 you are told you don't need to validate input, so the plain
`int(input(...))` is enough.

### 2.3 Arithmetic

```python
a + b        # add
a - b
a * b
a / b        # true division, always float (5/2 == 2.5)
a // b       # floor division (5//2 == 2)
a % b        # modulo
a ** b       # power
```

### 2.4 Comparisons and booleans

```python
a == b, a != b, a < b, a <= b, a > b, a >= b
not x, x and y, x or y
```

Short-circuit: `x and y` evaluates `y` only if `x` is truthy. Same as C.

### 2.5 `if` / `elif` / `else`

```python
if age > 60:
    print("Plant is ready to harvest!")
else:
    print("Plant needs more time to grow.")
```

No parentheses around the condition. The colon `:` opens a block. You can
nest `elif` as many times as needed.

### 2.6 Loops

```python
# while
i = 1
while i <= n:
    print(f"Day {i}")
    i += 1              # there is no i++ in Python

# for + range
for i in range(1, n + 1):    # 1, 2, ..., n (stop is exclusive)
    print(f"Day {i}")
```

`range(start, stop, step)` is the Pythonic counter. `range(n)` is `0..n-1`.

### 2.7 Functions

```python
def ft_hello_garden():
    print("Hello, Garden Community!")
```

- `def` defines a function.
- No return type syntax required (unless you add type hints).
- No `;`, no braces. The body is the indented block below `def ... :`.
- A function with no `return` statement returns `None` implicitly (like `void`).

**Recursion** works exactly like C — a function can call itself:

```python
def countdown(n):
    if n == 0:
        print("lift off!")
        return
    print(n)
    countdown(n - 1)
```

### 2.8 Type hints (ex7 only required)

```python
def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
    ...
```

Type hints are **annotations**, not enforcement. Python does not check them
at runtime — they are for humans and tools like `mypy`. The function still
runs if types don't match, so don't rely on them for validation.

Strings have useful methods:

```python
"tomato".capitalize()   # "Tomato"  — uppercase first letter
"HELLO".lower()         # "hello"
"hi".upper()            # "HI"
f"value = {x}"          # f-strings — interpolation
```

---

## 3. The 42 rules (read them until they stick)

From the PDF's General Instructions:

1. **Python 3.10+**.
2. **flake8** must pass. Stick to 4-space indent, no trailing whitespace, one
   blank line between functions.
3. Each exercise lives in its own file with the **exact** name the PDF says.
4. Each file contains **only the requested function** — no `if __name__ ==
   "__main__":`, no top-level calls, no prints outside the function.
5. Function names must match **exactly**: `ft_hello_garden`, not `hello` or
   `ft_Hello_Garden`.
6. Don't handle invalid input / negatives unless told to.
7. Type hints are required in ex7 (and checked by `mypy`).
8. The **only** imports/builtins allowed are listed per-exercise ("Authorized").
   In `ex4`, for example, the only allowed calls are `input()`, `int()`, `print()`.
   Using anything else (even `str()` or `sys.exit()`) is forbidden.

---

## 4. How to test your work

The PDF mentions a `main.py` helper. I've put a version in `examples/main.py`
that imports each of your exercise files and calls the function. Copy it into
the exercise folder you're testing:

```bash
cd exercises/ex0
cp ../../examples/main.py .
python3 main.py
```

For ex7, also run mypy to verify the type hints:

```bash
pip install mypy                      # once
mypy exercises/ex7/ft_seed_inventory.py
```

For style, install and run flake8:

```bash
pip install flake8
flake8 exercises/
```

---

## 5. Study plan

1. Read sections 1–2 of this file. Type out the examples in a REPL (`python3`).
2. Open `examples/01_syntax_tour.py`, run it, edit it, break it, fix it.
3. Tackle `exercises/ex0/ft_hello_garden.py`. Keep the PDF open.
4. Walk through ex1 → ex7 in order. Each one introduces exactly one new idea.
5. Only after you submit: open `solutions/` and diff against yours. Note
   anything you did differently and ask yourself whether the difference
   matters.

---

## 6. Mental model to carry into the rest of the course

- **Objects everywhere.** `5` is an `int` object. `"hi"` is a `str` object.
  Functions are objects. Classes are objects. This becomes important in
  modules 01, 05, 07 and 10.
- **Names are labels.** Assignment binds a name to an object; it does not
  copy. This will matter a lot when we hit mutable data in module 03.
- **Everything has a truthiness.** `if some_list:` is idiomatic for "is the
  list non-empty". Memorize this — you'll see it everywhere.

Ready? Go start `exercises/ex0/`.
