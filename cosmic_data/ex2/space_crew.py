from pydantic import (
    Field, ValidationError,
    BaseModel, model_validator)
from datetime import datetime
from enum import Enum


class CrewRank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(
        min_length=3, max_length=10
    )
    name: str = Field(
        min_length=2, max_length=50
    )
    rank: CrewRank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(
        min_length=3, max_length=30
    )
    years_experience: int = Field(
        ge=0, le=50
    )
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(
        min_length=5, max_length=15
        )
    mission_name: str = Field(
        min_length=3, max_length=100
    )
    destination: str = Field(
        min_length=3, max_length=50
    )
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(
        min_length=1, max_length=12
        )
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(
        ge=1.0, le=10000.0
    )

    @model_validator(mode="after")
    def check_miss_id(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError(
                "Mission ID must start with 'M'."
            )
        return self

    @model_validator(mode="after")
    def check_boss(self) -> "SpaceMission":
        has_boss: bool = False
        for member in self.crew:
            if member.rank in (CrewRank.COMMANDER, CrewRank.CAPTAIN):
                has_boss = True
        if not has_boss:
            raise ValueError(
                "Mission must have at least one"
                " Commander o Captain"
            )
        return self

    @model_validator(mode="after")
    def check_experienced_crew(self) -> "SpaceMission":
        experienced: int = 0
        if self.duration_days > 365:
            for member in self.crew:
                if member.years_experience >= 5:
                    experienced += 1
            if experienced < len(self.crew) / 2:
                raise ValueError(
                            "Long mission half crew with 5+ years "
                            "experience."
                )
        return self

    @model_validator(mode="after")
    def check_active_crew(self) -> "SpaceMission":
        for member in self.crew:
            if not member.is_active:
                raise ValueError(
                    "All crew members must be active."
                )
        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=============================")

    try:

        member1 = CrewMember(
            member_id="126",
            name="Carlos",
            rank=CrewRank.CAPTAIN,
            age=35,
            specialization="Developer",
            years_experience=10
        )
        member2 = CrewMember(
            member_id="1326",
            name="Anna",
            rank=CrewRank.COMMANDER,
            age=41,
            specialization="Physicist",
            years_experience=16
        )
        member3 = CrewMember(
            member_id="5126",
            name="Jane",
            rank=CrewRank.CADET,
            age=37,
            specialization="Technician",
            years_experience=6
        )
        spacemission = SpaceMission(
            mission_id="MC3-04",
            mission_name="Mars Chaos 3",
            destination="Mars",
            launch_date=datetime(2026, 10, 15),
            duration_days=730,
            crew=[member1, member2, member3],
            budget_millions=2000.0
        )
        print("Valid mission created:")
        print(f"Mission: {spacemission.mission_name}")
        print(f"ID: {spacemission.mission_id}")
        print(f"Destination: {spacemission.destination}")
        print(f"Duration: {spacemission.duration_days} days")
        print(f"Budget: ${spacemission.budget_millions}M")
        print(f"Crew size: {len(spacemission.crew)}")
        print("Crew members:")
        for member in spacemission.crew:
            print(
                f" - {member.name} ({member.rank}) - "
                f"{member.specialization}"
                )
    except ValidationError as e:
        print(f"Unexpected validation error:\n{e}")
    print("\n======================")
    print("Testing invalid mission:")

    try:
        member4 = CrewMember(
            member_id="CR004",
            name="Luca",
            rank=CrewRank.OFFICER,
            age=30,
            specialization="Engineer",
            years_experience=8
        )

        member5 = CrewMember(
            member_id="CR005",
            name="Marco",
            rank=CrewRank.CADET,
            age=25,
            specialization="Technician",
            years_experience=6
        )

        invalid_mission = SpaceMission(
            mission_id="M2026_TEST",
            mission_name="Mars Exploration",
            destination="Mars",
            launch_date=datetime(2026, 12, 15),
            duration_days=730,
            crew=[member4, member5],
            budget_millions=1500.0
        )

        print("Mission created!")
        print(invalid_mission)

    except ValidationError as e:
        print(f"Expected validation error:\n{e}")


if __name__ == "__main__":
    main()
