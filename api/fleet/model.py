from typing import Any
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class Fleets(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    app_short_code: str
    display_name: str
    customer_display_name: str
    fleet_location: Any
    google_cordinates: Any

class FleetSettings(BaseModel):
    id: int
    app_short_code: str
    fleet_location_template: str
