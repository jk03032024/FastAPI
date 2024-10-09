from typing import Any
from pydantic import BaseModel, Field
from uuid import uuid4, UUID

class MasterAccountCategories(BaseModel):
    id: int
    display_name: str

class MasterMicroServices(BaseModel):
    id: int
    display_name: str

class MasterPolicies(BaseModel):
    id: int
    microservice_display_name: str
    display_name: str
    claims: Any
    menu: Any
    permissions_required: bool

class MasterClaims(BaseModel):
    id: int
    feature_name: str
    display_name: str
    name: str
    type: str
    is_default_claim: bool
    microservice_display_name: str

