from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):

    name: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)
    userType : str = Field(default=None)
    fächer: list[str] = Field(default=None)
