from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("=" * 40)

    iss = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance="2024-08-15T10:00:00",  # type: ignore[arg-type]
        notes="All systems nominal.",
    )
    status = "Operational" if iss.is_operational else "Offline"
    print("Valid station created:")
    print(f"ID: {iss.station_id}")
    print(f"Name: {iss.name}")
    print(f"Crew: {iss.crew_size} people")
    print(f"Power: {iss.power_level}%")
    print(f"Oxygen: {iss.oxygen_level}%")
    print(f"Status: {status}")

    print()
    print("=" * 40)
    print("Expected validation error:")
    try:
        SpaceStation(
            station_id="BAD01",
            name="Over-crewed Station",
            crew_size=25,
            power_level=50.0,
            oxygen_level=50.0,
            last_maintenance=datetime(2024, 1, 1),
        )
    except ValidationError as exc:
        print(exc.errors()[0]["msg"])


if __name__ == "__main__":
    main()
