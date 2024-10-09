from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import Any

class Inventory(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    app_short_code: str
    asset_model_short_code: str
    child_device_short_code: str
    unique_id: str
    part_type: str
    part_code: str
    oem: str
    created_on: Any
    deployed_on: Any
    provisioned_on: Any
