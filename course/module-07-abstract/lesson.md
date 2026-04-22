# Module 07 — Abstract Classes (DataDeck)

> *"Program to an interface, not an implementation."*

Module 05 introduced abstract base classes as a way to force subclasses to
override specific methods. This module turns that one primitive into three
classical design patterns that keep large systems maintainable:

1. **Abstract Factory** — hide *which* concrete class is built behind a
   factory interface.
2. **Mixins / capabilities** — bolt extra orthogonal behaviour onto classes
   without bloating a single deep hierarchy.
3. **Strategy** — swap out *how* a class behaves at runtime by plugging in
   different strategy objects.

If you've done 42's CPP modules, you already know these patterns from
`new`-returning factory methods, interface classes, and function pointers.
The Python versions are lighter in ceremony but the same in spirit.

## 1. Abstract Factory

The factory pattern pairs a class hierarchy with a parallel factory
hierarchy. Callers never `Flameling()` directly — they ask the factory.

```python
import abc

class Creature(abc.ABC):
    def __init__(self, name: str, type_: str) -> None:
        self.name = name
        self.type_ = type_

    @abc.abstractmethod
    def attack(self) -> str: ...

    def describe(self) -> str:
        return f"{self.name} is a {self.type_} type Creature"


class CreatureFactory(abc.ABC):
    @abc.abstractmethod
    def create_base(self) -> Creature: ...
    @abc.abstractmethod
    def create_evolved(self) -> Creature: ...
```

Concrete classes `_Flameling`, `_Pyrodon` live inside the package but are
*not* re-exported — only `FlameFactory` is. That's the "package cannot
expose concrete Creature directly" rule: callers can only touch the family
via its factory.

Benefits:
- Add a new family (say `ElectricFactory`) without touching existing code.
- Swap a factory implementation for tests (fake creatures) trivially.

C/C++ analogue: a struct of function pointers returned by an initialiser
function. Same decoupling; less boilerplate in Python.

## 2. Capabilities (mixins) and multiple inheritance

Some behaviours cut across families. Healing and transforming aren't
fire-vs-water; they're orthogonal "capabilities" some creatures have.
Python lets a class inherit from multiple bases at once, so capabilities
become standalone abstract classes that concrete creatures mix in:

```python
class HealCapability(abc.ABC):
    @abc.abstractmethod
    def heal(self, target: typing.Any = None) -> str: ...


class TransformCapability(abc.ABC):
    def __init__(self) -> None:
        self._transformed: bool = False

    @abc.abstractmethod
    def transform(self) -> str: ...
    @abc.abstractmethod
    def revert(self) -> str: ...


class Shiftling(Creature, TransformCapability):
    def __init__(self) -> None:
        Creature.__init__(self, "Shiftling", "Normal")
        TransformCapability.__init__(self)
    ...
```

Because `Creature.__init__` and `TransformCapability.__init__` are
independent, calling them explicitly by name is the simplest way to keep
both parents happy (you can also set up cooperative `super()` chains with
`**kwargs`, but that's overkill for this project).

`isinstance(creature, TransformCapability)` is then a clean "does this
creature support transforming?" predicate — strategies use it to decide
validity.

### The diamond & MRO

Two parents, one `self`. Method lookup walks Python's **MRO** (Method
Resolution Order — C3 linearisation). You almost never need to think
about MRO unless both bases define the same method. Run
`Shiftling.__mro__` in a REPL if you're curious.

## 3. Strategy

Different creatures deserve different battle behaviour. Instead of
stuffing that logic into each creature (violating single-responsibility),
peel it out into a `BattleStrategy`:

```python
class BattleStrategy(abc.ABC):
    @abc.abstractmethod
    def is_valid(self, creature: Creature) -> bool: ...
    @abc.abstractmethod
    def act(self, creature: Creature) -> list[str]: ...
```

Concrete strategies decide which creatures they accept and what the "turn"
looks like:

- `NormalStrategy` — any creature; just calls `.attack()`.
- `DefensiveStrategy` — requires `HealCapability`; attack + heal.
- `AggressiveStrategy` — requires `TransformCapability`; transform, attack,
  revert.

Pairing a strategy with an incompatible creature should be an error with a
crisp message. A dedicated exception class keeps callers from catching the
wrong thing:

```python
class StrategyError(Exception):
    pass
```

## Pattern comparison (when to reach for which)

| Pattern           | Use when                                                    |
|-------------------|-------------------------------------------------------------|
| Factory           | Caller shouldn't know the concrete class                    |
| Mixin/capability  | Orthogonal behaviour shared by unrelated classes            |
| Strategy          | Same action done multiple ways depending on configuration   |
| Template method   | Skeleton algorithm in the base, steps overridden by subs    |

## Private-by-convention concrete classes

Python has no `private` keyword, but the leading underscore (`_Flameling`)
is a strong social signal: "don't import me directly." Combined with an
`__init__.py` that re-exports only the factories, that's the whole access
control story.

Check the `examples/01_patterns_tour.py` file for an end-to-end miniature
walk-through of all three patterns in a few dozen lines.
