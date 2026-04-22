"""Exercise 2 - SpaceMission with nested CrewMember list.

Enum: Rank {cadet, officer, lieutenant, captain, commander}

CrewMember fields:
- member_id, name, rank, age (18-80), specialization,
  years_experience (0-50), is_active=True.

SpaceMission fields:
- mission_id, mission_name, destination, launch_date,
  duration_days (1-3650), crew (list[CrewMember], 1-12),
  mission_status="planned", budget_millions (1.0-10000.0).

Mission rules (@model_validator(mode="after")):
- mission_id must start with "M".
- at least one Commander or Captain in the crew.
- if duration_days > 365, >= 50% of crew must have years_experience >= 5.
- every crew member must be active.
"""
from datetime import datetime
from enum import Enum
from typing_extensions import Self

from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    # TODO
    pass


class CrewMember(BaseModel):
    # TODO
    pass


class SpaceMission(BaseModel):
    # TODO: fields.

    @model_validator(mode="after")
    def _check_rules(self) -> Self:
        # TODO
        return self


def main() -> None:
    # TODO: build a valid 3-person Mars mission; print the summary.
    # TODO: build an invalid mission (no commander/captain);
    #       catch ValidationError and print the first error message.
    pass


if __name__ == "__main__":
    main()
