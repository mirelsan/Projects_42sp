from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, model_validator

class ContactType(str, Enum)
  radio = "radio"
  visual = "visual"
  physical = "physical"
  telepathic = "telepathic"

class AlienContact(BaseModel)
  contact_id: str = Field(min_length=5, max_length=15)
  timestamp: datetime
  location: str = Field(min_length=3, max_length=100)
  contact_type: ContactType
  signal_strenght: float = Field(ge=0.0, le=10.0)
  duration_minutes: int = Field(ge=1, le=1440)
  witness_count: int = Field(ge=1, le=100)
  message_received: Optional[str] = Field(default=None, max_length=500)
  is_verified: bool = Field(default=False)

  @model_validator(mode='after')
  def validate_alien_contact_rules(self) -> 'AlienContact':

    if not self.contact_id.startswitch("AC"):
      raise ValueError("Contact ID must start with 'AC'")

    if self.contact_type == ContactType.physical and not self.is_verified:
      raise ValueError("Physical contact reports must be verified")

    if self.contact_type == ContactType.telepathic and not self.verified:
      raise ValueError("Telepathic contact requires at least 3 witnesses")

    if self.signal_strength > 7.0 and not self.message_received:
      raise ValueError("Strong signals (>7.0) should include received messages")

  return self

def main() -> None:
  print("Alien Contact Log Validation\n")

  try:
    valid_contact = AlienContact(
      contact_id ="AC_2024_001",
      timestamp=datetime.now(),
      location="Area 51, Nevada",
      contact_type=ContactType.radio,
      signal_strenght=8.5,
      duration_minutes=45,
      witness_count=5,
      message_received="'Greetings from Zeta Reticuli'"
    )
    print("Valid Contact report:")
    print(f"ID: {valid_contact.contact.id}")
    print(f"Type: {valid_contact.contact_type}")
    print(f"Location: {valid_contact.location}")
    print(f"Signal: {contact_valid.signal_strenght}/10")
    print(f"Duration: {contact_valid.duration_minutes} minutes")
    print(f"Witness: {contact_valid.witness_count}")
      if valid_contact.message_received:
        print(f"Message: '{valid_contact.message_received}'\n")
  except ValidationError as e:
      print(f"Unexpected error: {e}")

    try:
      invalid_contact = AlienContact(
        contact_id ="AC_2024_001",
        timestamp=datetime.now(),
        location="Roswell, New Mexico",
        contact_type=ContactType.telepathic,
        signal_strenght=5.0,
        duration_minutes=10,
        witness_count=1,
      )
    except ValidationError as e:
      print("Expected validation error")

      for error in e.errors():
        print(error.get("msg").replace("Value error, ", ""))


if __name__ == "__main__":
    main()
