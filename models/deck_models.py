from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime
from typing import List
from uuid import UUID


class DeckRepo(BaseModel):
    deck_id: UUID
    deck_title: str
    first_entry_date: datetime
    last_entry_date: datetime
    provided_keywords: List[str] = Field(default_factory=list)
    generated_keywords: List[str] = Field(default_factory=list)
    all_entries_summary_sentence: str
    save_flag: bool
    priority: int

    # Validation for keywords: no duplicates
    @field_validator('provided_keywords', mode='after')
    def check_provided_keywords(cls, v):
        if not isinstance(v, list):
            raise TypeError('provided_keywords must be a list')
        if len(set(v)) != len(v):
            raise ValueError('provided_keywords contains duplicates')
        return v

    @field_validator('generated_keywords', mode='after')
    def check_generated_keywords(cls, v):
        if not isinstance(v, list):
            raise TypeError('generated_keywords must be a list')
        if len(set(v)) != len(v):
            raise ValueError('generated_keywords contains duplicates')
        return v

    # Validation for priority (must be between 1 and 100)
    @field_validator('priority')
    def priority_range(cls, v):
        if not (1 <= v <= 100):
            raise ValueError('priority must be between 1 and 100')
        return v

    # Validation that depends on fields (dates)
    @model_validator(mode='after')
    def check_dates(cls, model):
        if model.first_entry_date > model.last_entry_date:
            raise ValueError("first_entry_date cannot be after last_entry_date")
        return model
