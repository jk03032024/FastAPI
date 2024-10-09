from typing import Any, List, Set, Dict
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class AssetModels(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    app_short_code: str
    display_name: str
    short_code: str
    reference_image_url: str | None = None
    iot_architecture_url: str | None = None
    domain: str | None = None
    asset_general_category: str | None = None
    product_code: str | None = None
    oem: str | None = None
    field_deployment_template: str | None = None
    field_deployment_description: str | None = None
    contextual_data_to_be_captured: Any
    # primary_partitioning_template: str
    # secondary_partitioning_template: str | None = None
    # app_short_code: str
    # asset_mobile_stationary: str

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

class DataModel(BaseModel):
    child_device: List[Any] | None = None
    telemetry_model: List[Any] | None = None
    getset_model: List[Any] | None = None
    event_model: List[Any] | None = None
    contextual_model: List[Any] | None = None

class EdgeEventModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    app_short_code: str
    asset_model_short_code: str
    source_short_code: str
    source_type: str | None = None
    iothubdevice_short_code: str
    event_code: str
    event_message: str
    event_severity: str
    is_edge_ack_possible: bool | None = None
    is_cloud_ack_possible: bool | None = None
    is_edge_clr_possible: bool | None = None
    is_cloud_clr_possible: bool | None = None
    triggers: Any | None = None

class EdgeGetsetModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    app_short_code: str
    asset_model_short_code: str
    source_short_code: str
    source_type: str
    iothubdevice_short_code: str
    property_type: str | None = None
    property_json_key: str | None = None
    property_display_name: str | None = None
    property_data_type: str | None = None
    property_default_value: str | None = None
    property_min_value: str | None = None
    property_max_value: str | None = None
    property_enum: Set[str] | None = None
    property_unit: str | None = None
    property_accuracy: str | None = None

class EdgeTelemetryModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    app_short_code: str
    asset_model_short_code: str
    source_short_code: str
    source_type: str
    iothubdevice_short_code: str
    property_type: str
    property_json_key: str
    property_display_name: str
    property_data_type: str
    property_default_value: str
    property_min_value: str | None = None
    property_max_value: str | None = None
    property_enum: List[str] | None = None
    property_unit: str | None = None
    property_accuracy: str | None = None

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

class EdgeContexetualModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    app_short_code: str
    asset_model_short_code: str
    source_short_code: str | None = None
    source_type: str | None = None
    parameter_json_key: str | None = None
    parameter_display_name: str | None = None

class Widgets(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    app_short_code: str
    asset_model_short_code: str
    widget_code: str | None = None
    widget_type: str | None = None
    widget_size: str | None = None
    widget_color_theme: str | None = None
    widget_parameters: Any
    purpose: str | None = None

class NetworkInterfaces(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    app_short_code: str
    asset_model_short_code: str
    iothub_device_short_code: str | None = None
    lan_interface_available: bool | None = None
    wifi_interface_available: bool | None = None
    sim_interface_available: bool | None = None
    sim_type: str | None = None
    sim_size: str | None = None
