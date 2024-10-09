from typing import Any
from pydantic import BaseModel, Field
from uuid import uuid4, UUID


class Account_Types(BaseModel):
    # id: UUID = Field(default_factory=uuid4)
    id: int
    app_short_code: str
    display_name: str
    short_code: str
    account_category_display_name: str
    account_subcategory: str
    account_classification: str
    self_registration_allowed: bool
    parent_account_display_name: str | None = None

class AccountsAddress(BaseModel):
    country: str
    state: str
    city: str
    addressline1: str
    addressline2: str
    zipcode: str

class AccountsContactDetails(BaseModel):
    contactname: str
    contactemail: str
    contactnumber: str

class Accounts(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    app_short_code: str
    display_name: str
    account_category_display_name: str
    account_type_display_name: str
    account_subcategory: str | None = None
    address: AccountsAddress
    contactdetails: AccountsContactDetails
    logo_uri: str | None = None
    status: bool
    parent_id: None | UUID = Field(default_factory=uuid4)
    grandparent_id: None | UUID = Field(default_factory=uuid4) 

class Roles(BaseModel):
    id: int
    app_short_code: str
    account_type_name: str
    display_name: str
    is_it_admin_role: bool

class UserAccounts(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    account_id: str
    app_short_code: str
    user_email: str
    user_login: str
    user_fullname: str
    user_mobile: str
    user_globalid: str
    user_roleid: int
    user_status: bool
