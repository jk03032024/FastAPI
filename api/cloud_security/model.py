from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import Any

class CloudSecurityEvents(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    subscription_id: str | None = None
    subscription_name: str | None = None
    resource_group: str | None = None
    resource_type: str | None = None
    resource_name: str | None = None
    microsoft_alert_id: str | None = None
    alert_code: str | None = None
    alert_location: str | None = None
    alert_type: str | None = None
    activity_time_utc: Any
    alert_display_name: str | None = None
    alert_severity: str | None = None
    description: str | None = None
    remediation_steps: str | None = None
    detected_by: str | None = None
    azure_portal_alert_link: str | None = None
