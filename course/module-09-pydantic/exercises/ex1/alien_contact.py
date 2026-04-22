"""Exercise 1 - AlienContact model with a @model_validator.

Enum: ContactType {radio, visual, physical, telepathic}

Cross-field rules to enforce in @model_validator(mode="after"):
- contact_id must start with "AC".
- physical contacts require is_verified=True.
- telepathic contacts require witness_count >= 3.
- signal_strength > 7.0 requires a message_received.
"""
from datetime import datetime
from enum import Enum
from typing import Optional
from typing_extensions import Self

from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    # TODO
    pass


class AlienContact(BaseModel):
    # TODO: fields with Field(...) constraints.

    @model_validator(mode="after")
    def _check_rules(self) -> Self:
        # TODO: raise ValueError(...) on each rule violation.
        return self


def main() -> None:
    # TODO: build a valid radio contact; print summary.
    # TODO: build an invalid telepathic contact (witness_count=1);
    #       print the error message.
    pass


if __name__ == "__main__":
    main()
