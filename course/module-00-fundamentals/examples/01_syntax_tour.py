"""A guided tour of Python syntax for a C programmer.

Run me:   python3 01_syntax_tour.py
Then:     edit me, break me, fix me.
"""


# ── variables & types ────────────────────────────────────────────────
name = "tomato"       # str
count = 42            # int
mass = 1.5            # float
ripe = True           # bool  (capital!)
nothing = None        # like NULL, but a real object

print(type(name), type(count), type(mass), type(ripe), type(nothing))


# ── arithmetic ────────────────────────────────────────────────────────
print(7 / 2)    # 3.5   (true division)
print(7 // 2)   # 3     (floor)
print(7 % 2)    # 1
print(2 ** 10)  # 1024


# ── strings ───────────────────────────────────────────────────────────
s = "carrot"
print(s.upper())        # CARROT
print(s.capitalize())   # Carrot
print(f"{s} x {count}") # f-string interpolation


# ── input simulation (commented so the file runs unattended) ──────────
# line = input("Enter something: ")
# print("you typed:", line)


# ── if / elif / else ─────────────────────────────────────────────────
age = 75
if age > 60:
    print("ready to harvest")
elif age > 30:
    print("halfway there")
else:
    print("just a sprout")


# ── loops ────────────────────────────────────────────────────────────
for i in range(1, 4):     # 1, 2, 3
    print("day", i)

i = 0
while i < 3:
    print("w-step", i)
    i += 1


# ── functions ────────────────────────────────────────────────────────
def greet(who):
    print(f"hello, {who}!")


def double(x):
    return x * 2


greet("garden")
print(double(21))


# ── truthiness ───────────────────────────────────────────────────────
for value in [0, 1, "", "hi", [], [0], None]:
    print(repr(value), "->", bool(value))
