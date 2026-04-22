"""A mini-tour of Pydantic v2.

Requires pydantic>=2.

Run with:
    python3 01_pydantic_tour.py
"""
from datetime import datetime
from enum import Enum
from typing import Optional
from typing_extensions import Self

from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    model_validator,
)


class Role(str, Enum):
    reader = "reader"
    writer = "writer"
    admin = "admin"


class Address(BaseModel):
    city: str = Field(min_length=1)
    country: str = Field(min_length=2, max_length=2)


class User(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    age: int = Field(ge=0, le=150)
    role: Role = Role.reader
    email: Optional[str] = Field(
        default=None, pattern=r"^[^@]+@[^@]+\.[^@]+$"
    )
    joined: datetime
    address: Address

    @model_validator(mode="after")
    def admins_need_email(self) -> Self:
        if self.role == Role.admin and self.email is None:
            raise ValueError("Admins must provide an email address")
        return self


def main() -> None:
    alice = User(
        name="Alice",
        age=30,
        role="admin",
        email="alice@example.com",
        joined="2024-01-01T00:00:00",  # type: ignore[arg-type]
        address={"city": "Berlin", "country": "DE"},  # type: ignore[arg-type]
    )
    print("parsed ->", alice.model_dump())
    print("json   ->", alice.model_dump_json())

    print()
    print("=== Errors ===")
    for bad in (
        {"name": "Bob", "age": -1, "joined": "x", "address": {}},
        {
            "name": "Mallory",
            "age": 40,
            "role": "admin",
            "joined": datetime.now(),
            "address": {"city": "Zion", "country": "ZN"},
        },
    ):
        try:
            User.model_validate(bad)
        except ValidationError as exc:
            for err in exc.errors():
                loc = ".".join(str(p) for p in err["loc"])
                print(f"  {loc}: {err['msg']}")
            print()


if __name__ == "__main__":
    main()
