# Module 09 — Pydantic (Cosmic Data)

> *"Validate at the boundary; trust the core."*

Pydantic turns type hints into runtime contracts. You declare the shape
of your data with a class; Pydantic parses incoming dicts/JSON, checks
every field, raises a detailed `ValidationError` on bad input, and gives
you back a fully typed, attribute-access object.

If you've used C's `assert()`, `<stdbool.h>`-style invariants, or
hand-rolled JSON parsers that check every `cJSON_GetArrayItem`, you know
the pain. Pydantic collapses that into a handful of class definitions.

## BaseModel in 30 seconds

```python
from pydantic import BaseModel, Field
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    crew_size: int = Field(ge=1, le=20)
    last_maintenance: datetime
    is_operational: bool = True


iss = SpaceStation(
    station_id="ISS001",
    crew_size=6,
    last_maintenance="2024-08-15T10:00:00",  # str -> datetime (coerced)
)
print(iss.station_id)       # attribute access, typed
print(iss.model_dump())     # back to a dict
print(iss.model_dump_json())
```

- `Field(...)` is where you stash **constraints** (`ge`, `le`, `min_length`,
  `max_length`, `pattern`, `default`) and metadata (`description`,
  `examples`).
- Missing required fields: `ValidationError`.
- Wrong-shaped values: `ValidationError` with a precise path.
- Compatible types are coerced (ISO8601 string → `datetime`,
  `"42"` → `int` if the field is `int`; you can opt into strict mode
  with `model_config = ConfigDict(strict=True)`).

## The `Field` constraints you'll use in this module

| Constraint      | For              | Example                       |
|-----------------|------------------|-------------------------------|
| `min_length`    | `str`, `list`    | `Field(min_length=3)`         |
| `max_length`    | `str`, `list`    | `Field(max_length=50)`        |
| `ge` / `le`     | `int`, `float`   | `Field(ge=0, le=100)`         |
| `gt` / `lt`     | `int`, `float`   | `Field(gt=0)` (strict bound)  |
| `pattern`       | `str`            | `Field(pattern=r"^AC")`       |
| `default`       | anything         | `is_operational: bool = True` |

## Optional fields

`Optional[str]` means "either `str` or `None`". In Pydantic v2:

```python
from typing import Optional

notes: Optional[str] = Field(default=None, max_length=200)
```

`None` stays `None`; a string gets the `max_length` check.

## `model_validator(mode="after")` — cross-field rules

Field constraints handle single-value rules. For "if X then Y" logic
that needs to look at more than one field at a time, reach for a
**model-level validator**:

```python
from pydantic import BaseModel, model_validator
from typing import Self   # Python 3.11+


class AlienContact(BaseModel):
    contact_type: str
    witness_count: int
    is_verified: bool = False

    @model_validator(mode="after")
    def check_business_rules(self) -> Self:
        if self.contact_type == "physical" and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        if self.contact_type == "telepathic" and self.witness_count < 3:
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )
        return self
```

- Runs **after** per-field validation, so `self` already has fully
  parsed values of the right types.
- Return `self` (not `None`, not a dict).
- Raise `ValueError` to signal a violation — Pydantic wraps it into a
  `ValidationError` with the message attached.
- Pydantic 1's `@validator` is deprecated; use `@field_validator` (single
  field) or `@model_validator` (whole model) instead.

## Enums

Pydantic accepts Python `Enum` types directly — incoming strings are
mapped to enum members, and serialisation turns them back into their
values:

```python
from enum import Enum


class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_type: ContactType
```

`AlienContact(contact_type="radio")` works; `"sonar"` raises.

## Nested models

Put a model inside another and Pydantic recurses — validation, parsing,
and JSON round-tripping all just work:

```python
class CrewMember(BaseModel):
    name: str
    rank: Rank


class SpaceMission(BaseModel):
    mission_id: str
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
```

Pass `crew=[{"name": "...", "rank": "captain"}]` and Pydantic builds
`CrewMember` instances for you. A bad entry in the list raises with
`crew.2.rank` in the error path so you know exactly where the problem is.

## Catching validation errors

```python
from pydantic import ValidationError

try:
    SpaceStation(station_id="ISS001", crew_size=99, last_maintenance="...")
except ValidationError as exc:
    for error in exc.errors():
        print(error["loc"], error["msg"])
```

- `exc.errors()` returns a list of dicts, each with `loc` (path),
  `msg` (human text), `type` (machine id).
- `str(exc)` or `exc.json()` gives the pretty one-shot summary.

## v1 → v2 cheat sheet

| v1                            | v2                                  |
|-------------------------------|-------------------------------------|
| `@validator("field")`         | `@field_validator("field")`         |
| `@root_validator`             | `@model_validator(mode="...")`      |
| `.dict()`                     | `.model_dump()`                     |
| `.json()`                     | `.model_dump_json()`                |
| `parse_obj(...)`              | `model_validate(...)`               |
| `Config` inner class          | `model_config = ConfigDict(...)`    |
| `BaseSettings`                | `pydantic-settings` (separate pkg)  |

## C-to-Python mental model

- Field constraints = `assert(x >= 0 && x <= 100)` at the boundary.
- `ValidationError` = a structured version of `errno` with paths.
- Nested models = tagged structs; Pydantic owns both the parser and the
  type definitions.
- Type coercion = the library does the "parse int from string" dance for
  you so you never `strtol` by hand.

Install once with `pip install 'pydantic>=2,<3'` and you're good for
all three exercises.
