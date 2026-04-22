"""Exercise 0 - SpaceStation model with Pydantic v2.

Fields:
- station_id: str, 3-10 chars
- name: str, 1-50 chars
- crew_size: int, 1-20
- power_level: float, 0.0-100.0
- oxygen_level: float, 0.0-100.0
- last_maintenance: datetime
- is_operational: bool = True
- notes: Optional[str], max 200 chars

Demo: create one valid station, then try an over-crewed one and
print the ValidationError message.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    # TODO: add fields with the right Field(...) constraints.
    pass


def main() -> None:
    # TODO: create valid station; print a summary.
    # TODO: try invalid station (e.g. crew_size=25); catch ValidationError
    #       and print the first error message.
    pass


if __name__ == "__main__":
    main()
