# 42 Berlin — Python Rank 2 Course

An interactive, beginner-friendly Python course that takes you from zero to
completing every project in the 42 Berlin Rank 2 Python track. The course is
grounded in the real subject PDFs (`py-00.pdf` through `py-10.pdf` and
`Amazing.pdf`) sitting at the repo root — it doesn't invent parallel material.

> **You have a C background.** Each lesson calls out how a concept differs from
> C (memory, typing, indentation, duck typing, OOP, etc.) so you can map what
> you already know onto Python.

## How the course is organized

```
course/
├── README.md                ← you are here
├── .venv/                   ← your Python virtual environment (gitignored)
├── requirements.txt         ← shared dependencies (pydantic, pytest, etc.)
├── module-00-fundamentals/
│   ├── lesson.md            ← concepts + C-to-Python mapping
│   ├── examples/            ← tiny runnable demos
│   ├── exercises/           ← starter files YOU fill in (matches 42 names)
│   └── solutions/           ← reference solutions (DO NOT peek first)
├── module-01-oop/
│   └── ... same structure ...
├── ...
└── module-amazing-maze/
```

## The honor-system solutions policy

You chose option **B**: reference solutions live in `solutions/`. Write your
own in `exercises/` first. Only open `solutions/` **after** you've submitted
your work for peer review — otherwise you are cheating yourself out of the
learning, and risking a plagiarism flag at 42.

## Setup (once)

```bash
cd course
python3 -m venv .venv
source .venv/bin/activate        # or: source .venv/bin/activate.fish
pip install -r requirements.txt
```

To verify:

```bash
python --version                 # 3.10+ required
python -c "import pydantic; print(pydantic.VERSION)"
```

## Working on a module

```bash
cd module-00-fundamentals
# 1. Read lesson.md top-to-bottom
# 2. Run and tinker with files in examples/
# 3. Open exercises/ — these are the files you turn in.
#    File names and function signatures match the 42 PDF exactly.
# 4. Test your solutions. Each module includes a how-to-test section.
# 5. Only after submission: compare with solutions/
```

## The roadmap

| # | Module | Subject PDF | Core skills |
|---|---|---|---|
| 00 | Fundamentals (Growing Code) | `py-00.pdf` | variables, functions, control flow, type hints |
| 01 | OOP (Code Cultivation) | `py-01.pdf` | classes, inheritance, factory, encapsulation |
| 02 | Error handling (Garden Guardian) | `py-02.pdf` | try/except, custom errors, finally |
| 03 | Collections (Data Quest) | `py-03.pdf` | list/dict/set/tuple, comprehensions, generators |
| 04 | File I/O (Data Archivist) | `py-04.pdf` | open/read/write, streams, context managers |
| 05 | Polymorphism (Code Nexus) | `py-05.pdf` | abstract classes, method overriding, pipelines |
| 06 | Imports (The Codex) | `py-06.pdf` | packages, `__init__.py`, relative vs absolute |
| 07 | Abstract architectures (DataDeck) | `py-07.pdf` | ABCs, protocols, strategy pattern |
| 08 | Virtualenvs & packaging (The Matrix) | `py-08.pdf` | `venv`, `pip`, `requirements.txt`, `.env` |
| 09 | Pydantic (Cosmic Data) | `py-09.pdf` | models, validators, nested schemas |
| 10 | Functional programming (FuncMage) | `py-10.pdf` | lambda, HOF, decorators, recursion |
| ★ | Amazing — maze generator | `Amazing.pdf` | final capstone, combines everything |

## Submission rules (important!)

42 is strict about:

1. **Exact file names.** The names inside `exercises/` match the PDFs. Don't
   rename them.
2. **Forbidden imports.** Each lesson lists modules you are NOT allowed to
   import. Respect this — moulinette will fail you otherwise.
3. **No copy-paste from AI.** Re-type and understand every line. The PDFs
   themselves warn about this.
4. **Peer review.** Be ready to defend every line of every solution verbally.

Good luck, cadet.
