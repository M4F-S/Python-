# Module 07 — Exercise Workspace

Build three packages and three root-level test scripts:

```
exercises/
├── battle.py          # tests ex0
├── capacitor.py       # tests ex1
├── tournament.py      # tests ex2
├── ex0/               # Creature + CreatureFactory + concrete types
│   ├── __init__.py    # expose ONLY Creature + factories
│   ├── creatures.py
│   └── factories.py
├── ex1/               # HealCapability, TransformCapability, +factories
│   ├── __init__.py
│   ├── capabilities.py
│   ├── creatures.py
│   └── factories.py
└── ex2/               # strategies.py + StrategyError
    ├── __init__.py
    └── strategies.py
```

Run tests from this directory (it must be in `sys.path` so the ex*
packages resolve):

```
cd exercises
python3 battle.py
python3 capacitor.py
python3 tournament.py
```

Only peek at `../solutions/` after submitting. Honor system.
