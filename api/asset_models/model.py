from typing import Any, List, Dict
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class AssetModels(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    app_short_code: str
    display_name: str
    short_code: str
    reference_image_url: str | None = None
    iot_architecture_url: str | None = None
    domain: str
    asset_general_category: str
    product_code: str
    oem: str
    field_deployment_template: str
    field_deployment_description: str | None = None
    contextual_data_to_be_captured: Any

class ChildDevices(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    app_short_code: str
    asset_model_short_code: str
    display_name: str
    short_code: str
    part_type: str
    part_code: str
    oem: str
    protocol: str
    measurables: Any
    derivates: Any
    aggregates: Any
    read_only: Any
    read_write: Any
    event_codes: Any
    outputs: Any
    is_it_iothubdevice: bool
    routed_via: str
    contextual_data_to_be_captured: Any | None = None

class EdgeServices(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    app_short_code: str
    asset_model_short_code: str
    child_device_short_code: str
    display_name: str
    short_code: str
    service_type: str
    service_version: str
    publisher: str
    measurables: Any
    derivatives: Any
    aggregates: Any
    read_only: Any
    read_write: Any
    event_codes: Any
    contextual_data_to_be_captured: Any

class DataModel(BaseModel):
    child_device: List[Any] | None = None
    telemetry_model: List[Any] | None = None
    getset_model: List[Any] | None = None
    event_model: List[Any] | None = None
    contextual_model: List[Any] | None = None
