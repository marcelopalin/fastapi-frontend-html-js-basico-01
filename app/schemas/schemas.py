"""
    Description:

    - Pydantic Schemas

    Author:           @Palin
    Created:          2022-01-10
    Copyright:        (c) Ampere Consultoria Ltda
"""

from datetime import datetime

try:
    import uuid
    from typing import Optional

    from pydantic import BaseModel, EmailStr, Field, validator
except ImportError as error:
    print(error)
    print(f"error.name: {error.name}")
    print(f"error.path: {error.path}")


class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    username: str = Field(...)
    email: EmailStr = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "username": "John Doe",
                "email": "jdoe@example.com",
                "password": "pass@123",
            }
        }


class UserCreate(User):
    password: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "username": "John Doe",
                "email": "jdoe@example.com",
                "password": "pass@123",
            }
        }


class UserUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "username": "",
                "password": "",
            }
        }


class Estacao(BaseModel):
    DC_NOME: str
    VL_LATITUDE: str
    VL_LONGITUDE: str
    CD_ESTACAO: str
    CD_SITUACAO: str
    SG_ESTADO: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "DC_NOME": "ABROLHOS",
                "VL_LATITUDE": "17.96305555",
                "VL_LONGITUDE": "-38.70333333",
                "CD_ESTACAO": "A422",
                "CD_SITUACAO": "Pane",
                "SG_ESTADO": "BA",
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
