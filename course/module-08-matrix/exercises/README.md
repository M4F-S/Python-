# Module 08 — Exercise Workspace

Three exercises. Test your programs both inside and outside a venv, and
with / without dependencies.

```
exercises/
├── ex0/construct.py                # detect venv, print status
├── ex1/
│   ├── loading.py                  # pandas/numpy/matplotlib analysis
│   ├── requirements.txt
│   └── pyproject.toml
└── ex2/
    ├── oracle.py                   # env-var configuration via .env
    ├── .env.example
    └── .gitignore
```

Typical workflow:

```
# Exercise 0 — outside venv
cd ex0
python3 construct.py

# create a venv and run again
python3 -m venv matrix_env
source matrix_env/bin/activate
python construct.py
deactivate

# Exercise 1
cd ../ex1
pip install -r requirements.txt
python3 loading.py

# Exercise 2
cd ../ex2
cp .env.example .env
python3 oracle.py
MATRIX_MODE=production python3 oracle.py
```

Honor-system: skim `../solutions/` only after submitting.
