# Module 01 — Code Cultivation: Object-Oriented Garden Systems

> **Subject PDF:** `../../py-01.pdf`. Seven exercises that build one Plant
> class up from nothing into a full inheritance + analytics system.

---

## 1. New rule: type hints are mandatory

Unlike Module 00, **every function and method in Module 01 must have type
hints**. Run `mypy` on your files before submitting.

```python
def set_height(self, value: float) -> None: ...
def get_height(self) -> float: ...
```

Also new: you may (and should) include `if __name__ == "__main__":` test
blocks in each file. This is how the evaluator runs your code.

---

## 2. Python classes from a C mindset

C doesn't have classes; it has structs + free functions. Python classes are
that, plus:

- Methods automatically receive `self` (the instance pointer).
- Attributes are **attached at runtime** to `self` — no struct layout up
  front.
- Inheritance gives "free" code reuse.
- There's no real `private`. Conventions substitute for compiler
  enforcement.

### Minimal class

```python
class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name = name
        self.height = height
        self.age = age

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.age} days old")


p = Plant("Rose", 25.0, 30)
p.show()                          # Rose: 25.0cm, 30 days old
```

- `class Plant:` declares a new type.
- `__init__` is the constructor — called when you do `Plant(...)`.
- `self` is the first parameter of every instance method; you don't pass it,
  Python does. Think of it as an implicit first argument (like the
  `this` pointer in C++).
- You don't declare fields first — assigning `self.x = ...` inside `__init__`
  *creates* them.

### Dunder (magic) methods

`__init__`, `__str__`, `__repr__`, `__eq__`, etc. Double-underscore
("dunder") methods hook into Python syntax. In Module 01 you'll only need
`__init__`, but know the concept.

---

## 3. Encapsulation: the three conventions

Python has **no `private`**. Instead, there are three name conventions:

| Form | Name | Meaning |
|---|---|---|
| `self.x` | public | "use freely" |
| `self._x` | protected | "don't touch from outside unless you know what you're doing" |
| `self.__x` | name-mangled | Python actually rewrites it to `_ClassName__x` — creates soft isolation between parent and subclass |

The PDF explicitly tells you in Exercise 4 to **use the protected convention
(`_x`), not the mangling**. So write `self._height`, `self._age`, and expose
values only through `get_height()` / `set_height()`.

### Validated setters

```python
class Plant:
    def __init__(self, name: str, height: float = 0.0, age: int = 0) -> None:
        self._name = name
        self._height = 0.0
        self._age = 0
        self.set_height(height)
        self.set_age(age)

    def set_height(self, value: float) -> None:
        if value < 0:
            print(f"{self._name}: Error, height can't be negative")
            return
        self._height = float(value)

    def get_height(self) -> float:
        return self._height
```

Note how `__init__` calls `set_height` so the same validation runs both on
creation and on later updates.

---

## 4. Inheritance

```python
class Flower(Plant):
    def __init__(self, name: str, color: str,
                 height: float = 0.0, age: int = 0) -> None:
        super().__init__(name, height, age)   # call parent constructor
        self._color = color
        self._blooming = False

    def bloom(self) -> None:
        self._blooming = True

    def show(self) -> None:                   # method override
        super().show()                        # parent's show first
        print(f"Color: {self._color}")
        if self._blooming:
            print(f"{self._name} is blooming beautifully!")
        else:
            print(f"{self._name} has not bloomed yet")
```

- `class Flower(Plant):` makes Flower inherit everything from Plant.
- `super().__init__(...)` runs the parent constructor. Without this you
  won't have `_name`, `_height`, `_age`.
- Overriding `show` and calling `super().show()` reuses code instead of
  duplicating it. The PDF explicitly rewards this in ex5.

### Method Resolution Order (MRO)

If `Flower` extends `Plant`, Python looks up attributes on `Flower` first,
then `Plant`, then `object`. For simple linear inheritance this is obvious;
it gets interesting with multiple inheritance (covered briefly in Module 07).

---

## 5. Static and class methods (ex6)

```python
class Plant:
    @staticmethod
    def is_older_than_one_year(age_days: int) -> bool:
        return age_days > 365

    @classmethod
    def anonymous(cls) -> "Plant":
        return cls("Unknown plant")
```

- `@staticmethod`: plain function that lives inside the class namespace. No
  `self`, no `cls`. Use for logic that belongs to the concept but doesn't
  need an instance.
- `@classmethod`: receives the class itself (`cls`) as first argument,
  instead of an instance. Use for alternative constructors. `cls(...)` works
  polymorphically — if a subclass calls `Plant.anonymous()`, `cls` is the
  subclass.

---

## 6. Nested classes (ex6)

You can declare a class inside another class. It has no special "I belong to
my outer class" scope — it's just a name defined in that namespace. Useful
for bundling helper types.

```python
class Plant:
    class _Stats:
        def __init__(self) -> None:
            self._grow = 0
            self._age = 0
            self._show = 0

        def display(self) -> None:
            print(f"Stats: {self._grow} grow, "
                  f"{self._age} age, {self._show} show")

    def __init__(self, name: str) -> None:
        self._name = name
        self._stats = Plant._Stats()

    def grow(self) -> None:
        self._stats._grow += 1
        self._height += 1.0
```

Extending the nested class in a subclass is tricky but possible — see the
ex6 solution for the Tree variant with a `_shade` counter.

---

## 7. Strategy for this module

The PDF builds one class across seven files. **Each exercise can copy the
previous one** and extend it. Don't rewrite from scratch.

Suggested rhythm:

1. ex0: Just print. Practice `if __name__ == "__main__":`.
2. ex1: Write `Plant` with `__init__` + `show()`.
3. ex2: Add `grow()` and `age()`. Think about how `height` changes over time.
4. ex3: You already did this if you wrote `__init__` in ex1. The PDF
   acknowledges this.
5. ex4: Rename `self.height` → `self._height` and introduce
   getters/setters with validation.
6. ex5: Subclass into `Flower`, `Tree`, `Vegetable`. Every subclass
   overrides `show()` and calls `super().show()`.
7. ex6: The big one. Add statics, classmethods, a nested `_Stats` class,
   a `Seed` subclass of `Flower`, and a top-level `display_stats(plant)`
   function that works for any plant type.

### Forbidden-list reminders

- ex0–4: `print()`, `range()`, `round()` only (plus `class`/`def` which
  don't count).
- ex5: adds `super()`.
- ex6: adds `staticmethod()` / `classmethod()` (or their decorator form).

You cannot import anything. No `math`, no `sys`, no `typing` helpers
beyond built-in type hints (`int`, `str`, `float`, `bool`, `list`, `None`).

---

## 8. Testing

```bash
cd exercises/ex1 && python3 ft_garden_data.py
mypy ft_garden_data.py
flake8 ft_garden_data.py
```

Good luck.
