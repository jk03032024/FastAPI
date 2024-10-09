from typing import Any, List
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class Tickets(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    app_short_code: str
    category: str
    problem_statement: str
    alloted_to: str | None = None
    original_email: Any
    contact_details_mentioned_in_email: Any
    # custumer_id: UUID = Field(default_factory=uuid4)
    # customer_display_name: str
    # contact_details: Any
    ai_diagnostics: Any
    ai_prescriptions: Any
    job_summary: str | None = None
    media_uploads: Any
    current_status: str | None = None
    created_by: str | None = None
    created_on: Any | None = None
    updated_by: str | None = None
    updated_on: Any | None = None
    ticket_created_by: str| None = None
    ticket_updated_by: None | UUID = Field(default_factory=uuid4)
    ticket_short_code: str | None = None
    assigned_to: str | None = None
    customer_fullname: str | None = None

class MediaUpload(BaseModel):
    name: str
    url: str

class OriginalEmail(BaseModel):
    senderemail: str
    emailtime: str
    emailtext: str
    emailattachments: List[MediaUpload]

class TicketCreateRequest(BaseModel):
    app_short_code: str
    category: str
    problem_statement: str
    original_email: OriginalEmail
    ai_diagnostics: Any | None = None
    ai_prescriptions: Any | None = None

    # media_uploads: list[dict]