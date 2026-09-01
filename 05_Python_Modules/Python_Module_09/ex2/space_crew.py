from enum import Enum
from typing import List
from datetime import datetime
from pydantic import BaseModel, Fiel, ValidationError, model_validator

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
  is_active: bool = Field(default=True)

class SpaceMission(BaseModel):
  mission_id: str = Field(min_length=5, max_length=15)
  mission_name: str = Field(min_length=3, max_length=100)
  destination: str = Field(min_length=3, max_length=50)
  launch_date: str = datetime
  duration_days: int = Field(ge=1, le=3650)
  crew: List[CrewMember] = Field(min_length=1, max_length=12)
  mission_status: str = Field(default="planned")
  budget_millions: float = Field(ge=1.0, leg=10000.0)

@model_validator(mode='after')
  def validate_mission_requirements(self) -> 'SpaceMisson':

    if not self.mission_id.startswith('M'):
      raise ValueError("Mission ID must start with 'M'")

    for member in self.crew:
      if not member.is_active:
        raise ValueError("All crew members must be active")

    has_leadership = any(member.rank in [Rank.commander, Rank.captain] for member in self.crew)
    if not has_leadership:
      raise ValueError("Mission must have at least one Commander or Captain")

    if self.duration_days > 365:
      experienced_members = sum(1 for member in self.crew if member.years_experience >= 5)
      if experienced_members < (len(self.crew) / 2):
          raise ValueError("Long missions require 50% experienced crew (5+ years)")

    return self


def main() -> None:
  print("Space Mission Crew Validation\n")
  print("===============================")

  sarah = CrewMember(
      member_id="C001", name="Sarah Connor", rank=Rank.commander,
      age=45, specialization="Mission Command", years_experience=15
  )
  john = CrewMember(
      member_id="C002", name="John Smith", rank=Rank.lineutenant,
      age=32, specialization="Navigation", years_experience=8
  )
  alice = CrewMember(
    member_id="C003", name="Alice Johnson", rank=Rank.officer,
    age=28, spacialization="Engineering", years_experience=4
  )
  bob = CrewMember(
    member_id="C004", name="BOB NOOB", rank=Rank.cadet,
    age=22, specialization="Botany", years_experience=1
  )

  try:
    valid_mission = SpaceMission(
      mission_id="M2024_MARS",
      mission_name="Mars Colony Establishment",
      destination="Mars",
      launch_date=datetime.now(),
      duration_days=900,
      budget_millions=2500.0,
      crew=[sarah, john, alice]
    )
    print("Valid mission created:")
    print(f"Mission: {valid_mission.mission_name}")
    print(f"ID: {valid_mission.mission_id}")
    print(f"Destination: {valid_mission.destination}")
    print(f"Duration: {valid_mission.duration_days}")
    print(f"Budget: {valid_mission.budget_millions}")
    print(f"Crew size: {len(valid_mission.crew)}")
    print(f"Crew members:")
    for c in valid_mission.crew:
      print(f"- {c.name} ({c.rank.value}) - {c.specialization}")
    print("\n")

  except ValidationError as e:
    print("Expected validation error:")
    for error in e.errors():
      print(error.get("msg").replace("Value error, ", ""))

if __name__ == "__main__":
  main()
