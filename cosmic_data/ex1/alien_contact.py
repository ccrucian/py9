from pydantic import (
    Field, BaseModel,
    ValidationError, model_validator)
from datetime import datetime
from typing import Optional
from enum import Enum


# Enum serve a definire un valore preciso di valori consentiti
class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def check_contact_id(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError(
                "Contact ID must start with AC"
                )
        return self

    @model_validator(mode="after")
    def check_physical_contact(
            self) -> "AlienContact":
        if self.contact_type.value == "physical":
            if not self.is_verified:
                raise ValueError(
                    "Physical contact must be verified."
                )
        return self

    @model_validator(mode="after")
    def check_telepathic_contact(
            self) -> "AlienContact":
        if self.contact_type.value == "telepathic":
            if self.witness_count < 3:
                raise ValueError(
                    "Telepathic contact requires "
                    "at least 3 witnesses"
                )
        return self

    @model_validator(mode="after")
    def check_strong_signal(
            self) -> "AlienContact":
        if self.signal_strength > 7.0:
            if not self.message_received:
                raise ValueError(
                    "Strong signal should include "
                    "received messages."
                )
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("=============================")
    try:
        contact1 = AlienContact(
            contact_id="AC in the sky",
            timestamp=datetime(2026, 10, 15),
            location="Grotarossa",
            contact_type=ContactType.PHYSICAL,
            signal_strength=8.0,
            duration_minutes=2,
            witness_count=6,
            message_received="Fuck you",
            is_verified=True
        )
        print("Valid contact report:")
        print(f"ID: {contact1.contact_id}")
        print(f"Type: {contact1.contact_type.value}")
        print(f"Location: {contact1.location}")
        print(f"Signal: {contact1.signal_strength}/10")
        print(f"Duration: {contact1.duration_minutes}")
        print(f"Witnesses: {contact1.witness_count}")
        print(f"Message: '{contact1.message_received}'")
    except ValidationError as e:
        print(f"Validation error: {e}")
        print("=======================")
    print("\nTesting invalid contact report:")
    try:
        contact2 = AlienContact(
            contact_id="AC Met Ugo",
            timestamp=datetime(2026, 10, 15),
            location="car",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=2,
            duration_minutes=2,
            witness_count=2,
            message_received="Singing a song",
            is_verified=True
            )
        print(contact2)
    except ValidationError as e:
        print(f"Expected validation error:\n{e}")


if __name__ == "__main__":
    main()
