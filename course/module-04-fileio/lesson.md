# Module 04 — Data Archivist: File I/O

> **Subject PDF:** `../../py-04.pdf`. Four exercises on `open()`, reading,
> writing, `stdin`/`stdout`/`stderr`, and the `with` statement.

---

## 1. `open()` in 30 seconds

In C: `FILE *f = fopen(name, mode)`, then `fread`, `fwrite`, `fclose`.
Python is the same shape:

```python
f = open("note.txt", "r")     # modes: "r", "w", "a", "rb", "wb", ...
data = f.read()               # whole file as str
line = f.readline()           # one line
f.write("hello\n")
f.close()
```

- `"r"` read text (default). Fails if file missing — `FileNotFoundError`.
- `"w"` write text. **Truncates existing file.**
- `"a"` append.
- Add `"b"` for binary: `"rb"`, `"wb"`. Returns `bytes` instead of `str`.

`open()` returns an `IO` object. Its full type is `typing.IO[str]` for
text mode. Per the ex0 authorized list, that's the import to use.

### Exception family

| When | Exception |
|---|---|
| File missing | `FileNotFoundError` |
| Permission denied | `PermissionError` |
| Any OS error | `OSError` (parent of both above) |

Put your `open()` inside `try/except OSError as e:` so one clause catches
both "missing" and "denied".

### Read strategies

```python
f.read()                  # whole file
f.readlines()             # list[str], keeping "\n"
for line in f: ...        # iterates line by line (streaming)
```

Every read advances the cursor; after `f.read()` the file is exhausted.

---

## 2. The three standard streams

Coming from C you know `stdin`/`stdout`/`stderr`. Python exposes them via
`sys`:

```python
import sys

print("hello")                              # -> stdout
print("boom", file=sys.stderr)              # -> stderr
line = sys.stdin.readline()                 # read a line, includes "\n"
sys.stdout.write("no newline added\n")
sys.stdout.flush()
```

In ex2 you are **not allowed to use `input()`**. Use
`sys.stdin.readline()` — remember to `strip()` the trailing newline, or
use `line.rstrip("\n")`.

Write errors to `stderr` like this:

```python
print(f"[STDERR] Error opening file {name!r}: {e}", file=sys.stderr)
```

---

## 3. The `with` statement (ex3 only)

Context manager: "run this block, guarantee cleanup no matter what".

```python
with open("note.txt", "r") as f:
    data = f.read()
# here the file is already closed, even if an exception was raised
```

Equivalent to:

```python
f = open("note.txt", "r")
try:
    data = f.read()
finally:
    f.close()
```

Much cleaner. In ex3 you **must** use `with`. In ex0-2, you must **not** use
`with` — the subject explicitly saves it for ex3.

---

## 4. The module's progression

| # | File | Adds |
|---|---|---|
| 0 | `ft_ancient_text.py` | `sys.argv`, `open("r")`, `.read()`, catch errors, `.close()` |
| 1 | `ft_archive_creation.py` | Transform content (append `#` to lines), `input()`, `open("w")`, `.write()` |
| 2 | `ft_stream_management.py` | Errors → `stderr`; replace `input()` with `sys.stdin.readline()` |
| 3 | `ft_vault_security.py` | One `secure_archive()` function using `with open(...)` |

Each exercise copies the previous file and extends it. Don't rewrite.

---

## 5. The `secure_archive` signature (ex3)

```python
def secure_archive(
    filename: str,
    action: str = "read",
    content: str = "",
) -> tuple[bool, str]:
    ...
```

- `action == "read"` → try to read and return `(True, contents)`.
- `action == "write"` → try to write `content` and return `(True, "Content successfully written to file")`.
- On any OS error → `(False, str(error))`.

Use `with open(...)` inside the function. Let exceptions trigger the
`(False, ...)` return path.

---

## 6. Gotchas to watch

- **Write mode truncates.** `open("x", "w")` erases the file before you
  write. Use `"a"` (append) if that's what you want.
- **Newlines are your responsibility.** `write` does NOT add one.
- **A closed file still has a name.** You can `print(f.name)` after close
  if you saved a reference before closing.
- **`typing.IO` typing.** Use `typing.IO` for the generic, `typing.TextIO`
  or `typing.BinaryIO` for specifics. In ex0/1/2 the authorized list names
  `typing.IO`, so:
  ```python
  from typing import IO
  def open_it(name: str) -> IO[str] | None: ...
  ```
- **flake8 wants f.close() inside the except-else flow.** When open
  succeeds but read fails, close anyway. Or just use try/finally.

---

## 7. Testing

Create `ancient_fragment.txt` beside each exercise:

```
[FRAGMENT 001] Digital preservation protocols established 2087
[FRAGMENT 002] Knowledge must survive the entropy wars
[FRAGMENT 003] Every byte saved is a victory against oblivion
```

Then:

```bash
python3 ft_ancient_text.py ancient_fragment.txt
python3 ft_ancient_text.py nope           # missing path
python3 ft_ancient_text.py /etc/shadow    # permission denied
mypy ft_ancient_text.py
flake8 ft_ancient_text.py
```
