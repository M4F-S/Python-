from datetime import datetime
from enum import Enum
from typing_extensions import Self

from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def _check_rules(self) -> Self:
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")
        if not any(
            c.rank in (Rank.captain, Rank.commander) for c in self.crew
        ):
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )
        if self.duration_days > 365:
            experienced = sum(
                1 for c in self.crew if c.years_experience >= 5
            )
            if experienced * 2 < len(self.crew):
                raise ValueError(
                    "Long missions (> 365 days) need at least "
                    "50% experienced crew (5+ years)"
                )
        if not all(c.is_active for c in self.crew):
            raise ValueError("All crew members must be active")
        return self


def _first_error(exc: ValidationError) -> str:
    msg = exc.errors()[0]["msg"]
    return msg.removeprefix("Value error, ")


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 41)

    crew = [
        CrewMember(
            member_id="C001",
            name="Sarah Connor",
            rank=Rank.commander,
            age=42,
            specialization="Mission Command",
            years_experience=18,
        ),
        CrewMember(
            member_id="C002",
            name="John Smith",
            rank=Rank.lieutenant,
            age=35,
            specialization="Navigation",
            years_experience=10,
        ),
        CrewMember(
            member_id="C003",
            name="Alice Johnson",
            rank=Rank.officer,
            age=29,
            specialization="Engineering",
            years_experience=6,
        ),
    ]

    mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime(2024, 12, 1),
        duration_days=900,
        crew=crew,
        budget_millions=2500.0,
    )

    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for c in mission.crew:
        print(f"- {c.name} ({c.rank.value}) - {c.specialization}")

    print()
    print("=" * 41)
    print("Expected validation error:")
    junior_crew = [
        CrewMember(
            member_id="C010",
            name="Bob Junior",
            rank=Rank.officer,
            age=28,
            specialization="Support",
            years_experience=3,
        ),
        CrewMember(
            member_id="C011",
            name="Eve Novice",
            rank=Rank.cadet,
            age=21,
            specialization="Navigation",
            years_experience=1,
        ),
    ]
    try:
        SpaceMission(
            mission_id="M2024_BAD",
            mission_name="Rudderless Expedition",
            destination="Europa",
            launch_date=datetime(2024, 12, 1),
            duration_days=120,
            crew=junior_crew,
            budget_millions=100.0,
        )
    except ValidationError as exc:
        print(_first_error(exc))


if __name__ == "__main__":
    main()
