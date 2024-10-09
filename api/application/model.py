from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class Application(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    display_name: str
    short_code: str
    description: str
    domain: str
    icon_uri: str
    created_by: str
    updated_by: str
    created_at: datetime
    updated_at: datetime
    is_site: bool | None = None
    is_fleet: bool | None = None
    is_super_asset: bool | None = None
