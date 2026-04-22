# Module 09 — Exercise Workspace

Install Pydantic 2 first (inside a venv):

```
pip install 'pydantic>=2,<3'
```

Then:

```
python3 ex0/space_station.py
python3 ex1/alien_contact.py
python3 ex2/space_crew.py
```

Three progressive exercises:

1. **ex0** — basic `BaseModel` + `Field` constraints + datetime coercion.
2. **ex1** — cross-field rules with `@model_validator(mode="after")`, Enums.
3. **ex2** — nested models (`CrewMember` inside `SpaceMission`) + complex
   business rules.

Honor-system: don't peek at `../solutions/` until you've submitted.
