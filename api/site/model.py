from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class SitesSiteLocation(BaseModel):
    country: str
    state: str
    city: str
    Area: str
    Building: str

class SitesGoogleCordinates(BaseModel):
    latitude: str
    longitude: str

class Sites(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    app_short_code: str
    display_name: str
    customer_display_name: str
    site_location: SitesSiteLocation
    google_cordinates: SitesGoogleCordinates

class SiteSettings(BaseModel):
    id: int
    app_short_code: str
    site_location_template: str
    insidesite_location_template: str
