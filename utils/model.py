from pydantic import BaseModel, ConfigDict

class UserID(BaseModel):
    model_config = ConfigDict(extra="forbid")
    user_id: str
