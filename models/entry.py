from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime
from typing import Optional


class Entry(BaseModel):
    entry_id: Optional[str] = None  # Optional internal ID or UUID
    message_id: int  # Telegram message ID
    user_id: int  # Telegram user ID
    username: Optional[str] = None  # Username of the sender
    chat_id: int  # Chat ID (private or group)
    timestamp: datetime  # When the message was sent
    text: Optional[str] = None  # Text content of the message, if any
    raw_message: Optional[dict] = None  # Raw Telegram message JSON (optional)
    media_type: Optional[str] = None  # Type of media: "text", "photo", "voice", etc.
    media_file_id: Optional[str] = None  # File ID for media download, if any
    star_flag: bool = False  # Flag to mark important entries

    # Example validation: media_type must be one of expected values or None
    @field_validator('media_type')
    def validate_media_type(cls, v):
        allowed_types = {None, "text", "photo", "voice", "document", "video", "audio"}
        if v not in allowed_types:
            raise ValueError(f"media_type '{v}' is not valid")
        return v

    # Example model-level validation: text or media_file_id should be present
    @model_validator(mode='after')
    def check_content_presence(cls, model):
        if not model.text and not model.media_file_id:
            raise ValueError("Entry must have either text or media_file_id")
        return model
