from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime
from typing import Optional


class EntryRepo(BaseModel):
    entry_id: str  # Optional internal ID or UUID
    message_id: int  # Telegram message ID
    user_id: int  # Telegram user ID
    username: Optional[str] = None  # Username of the sender
    timestamp: datetime  # When the message was sent
    text: Optional[str] = None  # Text content of the message, if any
    raw_message: Optional[dict] = None  # Raw Telegram message JSON (optional)
    media_type: Optional[str] = None  # Type of media: "text", "photo", "voice", etc.
    deck_id: Optional[str] = None
    save_flag: bool = False  # Flag to mark important entries

    # Example validation: media_type must be one of expected values or None
    @field_validator('media_type')
    def validate_media_type(cls, v):
        allowed_types = {None, "text"}
        if v not in allowed_types:
            raise ValueError(f"media_type '{v}' is not valid")
        return v

    @model_validator(mode='after')
    def check_content_presence(cls, model):
        if not model.text:
            raise ValueError("Entry must have text")
        return model
