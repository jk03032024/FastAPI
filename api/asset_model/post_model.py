from typing import Any, List, Set, Dict
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class InsertContextualParameters(BaseModel):
    parameterjsonkey: str | None = None
    parameterdisplayname: str | None = None

class ContextualParameters(BaseModel):
    contextualparameters: List[InsertContextualParameters] | None = None

class InserReadOnly(BaseModel):
    propertyjsonkey: str | None = None
    propertyname: str | None = None
    propertyunits: str | None = None
    propertytype: str | None = None
    propertyenum: Set[str] | None = None
    propertydatatype: str | None = None
    propertydefaultvalue: float | str | None = None
    propertyminvalue: float | str | None = None
    propertymaxvalue: float| str | None = None
    propertyprecision: float | str | None = None
    propertyaccuracy: float | str | None = None

class ReadOnly(BaseModel):
    readonly: List[InserReadOnly] | None = None

class InsertEventCodes(BaseModel):
    eventcode: str | None = None
    eventmessage: str | None = None
    eventseverity: str | None = None

class Events(BaseModel):
    events: List[InsertEventCodes] | None = None

class WidgetParameters(BaseModel):
    propertyjsonkey: str | None = None

class InsertMeasurables(BaseModel):
    propertyjsonkey: str | None = None
    propertyname: str | None = None
    propertyunits: str | None = None
    propertytype: str | None = None
    propertyenum: Set[str] | None = None
    propertydatatype: str | None = None
    propertydefaultvalue: float | str | None = None
    propertyminvalue: float | str | None = None
    propertymaxvalue: float| str | None = None
    propertyprecision: float | str | None = None
    propertyaccuracy: float | str | None = None

class Measurables(BaseModel):
    measurables: List[InsertMeasurables] | None = None

class InsertReadWrite(BaseModel):
    propertyjsonkey: str | None = None
    propertyname: str | None = None
    propertyunits: str | None = None
    propertytype: str | None = None
    propertyenum: Set[str] | None = None
    propertydatatype: str | None = None
    propertydefaultvalue: float | str | None = None
    propertyminvalue: float | str | None = None
    propertymaxvalue: float | str | None = None
    propertyaccuracy: float | str | None = None

class ReadWrite(BaseModel):
    configurables: List[InsertReadWrite] | None = None

class InsertWidget(BaseModel):
    asset_model_short_code: str | None = None
    widget_type: str | None = None
    widget_size: str | None = None
    widget_color_theme: str | None = None
    widget_parameters: WidgetParameters
    purpose: str | None = None

class InsertTelemetryModel(BaseModel):
    asset_model_short_code: str | None = None
    source_short_code: str
    source_type: str | None = None
    iothubdevice_short_code: str | None = None

class InsertService(BaseModel):
    asset_model_short_code: str | None = None
    display_name: str | None = None
    short_code: str | None = None
    service_type: str | None = None
    service_version: str | None = None
    publisher: str | None = None
    measurables: Measurables | None = None
    derivatives: Any
    aggregates: Any
    read_only: ReadOnly | None = None
    read_write: ReadWrite | None = None
    event_codes: Events | None = None
    contextual_data_to_be_captured: ContextualParameters | None = None

class InsertGetSetModel(BaseModel):
    asset_model_short_code: str | None = None
    source_short_code: str
    source_type: str | None = None
    iothubdevice_short_code: str | None = None

class InsertEventModel(BaseModel):
    is_edge_ack_possible: bool | None = None
    is_cloud_ack_possible: bool | None = None
    is_edge_clr_possible: bool | None = None
    is_cloud_clr_possible: bool | None = None
    triggers: Any

class InsertContextualModel(BaseModel):
    asset_model_short_code: str | None = None
    source_short_code: str
    source_type: str | None = None
    parameter_json_key: str | None = None
    parameter_display_name: str | None = None

class InsertChildDevice(BaseModel):
    asset_model_short_code: str | None = None
    display_name: str | None = None
    short_code: str | None = None
    part_type: str | None = None
    part_code: str | None = None
    oem: str | None = None
    protocol: str | None = None
    measurables: Measurables | None = None
    derivatives: Any
    aggregates: Any
    read_only: ReadOnly | None = None
    read_write: ReadWrite | None = None
    event_codes: Events | None = None
    outputs: Any
    is_it_iothubdevice: bool | None = None
    routed_via: str | None = None
    contextual_data_to_be_captured: ContextualParameters | None = None

class InsertAssertModel(BaseModel):
    display_name: str | None = None
    short_code: str | None = None
    reference_image_url: str | None = None
    iot_architecture_url: str | None = None
    domain: str | None = None
    asset_general_category: str | None = None
    product_code: str | None = None
    oem: str | None = None
    field_deployment_template: str | None = None
    field_deployment_description: str | None = None
    contextual_data_to_be_captured: ContextualParameters | None = None

class InsertDataModel(BaseModel):
    asset_model: InsertAssertModel
    child_devices: InsertChildDevice
    event_model: InsertEventModel
    service_model: InsertService
