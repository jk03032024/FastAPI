from typing import Any, Dict
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class Assets(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    app_short_code: str
    asset_model_short_code: str | None = None
    display_name: str
    no_of_linked_iothubdevices: Any | None = None
    customer_display_name: str | None = None
    site_location: Any | None = None
    fleet_location: Any | None = None
    superasset_display_name: Any | None = None
    contextual_data_captured: Any
    image_uri: str | None = None

class AssetWiseIothubdevices(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    app_short_code: str
    asset_id: UUID = Field(default_factory=uuid4)
    iothubdevice_unique_id: str
    iothubdevice_short_code: str
    asset_model_short_code: str

class ContextualMetadata(BaseModel):
    asset_model: Any
    installed_location: Any
    location_cordinates: Any
    unique_id: Any
    commissioned_on: Any
    oem: Any
    asset_image: Any
    product_code: Any
    product_type: Any

class AssetsContextualMetadata(BaseModel):
    contextual_data_captured: ContextualMetadata
