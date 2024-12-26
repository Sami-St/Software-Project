from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class User(BaseModel):

    userID: Optional[int] = None
    name: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)
    rolle : str = Field(default=None)
    fächer: list[str] = Field(default=None)
