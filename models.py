from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class User(BaseModel):
    email: EmailStr
    phone: str
    fam: str
    name: str
    otc: Optional[str] = ""


class Coords(BaseModel):
    latitude: float
    longitude: float
    height: int


class Level(BaseModel):
    winter: Optional[str] = ""
    summer: Optional[str] = ""
    autumn: Optional[str] = ""
    spring: Optional[str] = ""


class Image(BaseModel):
    title: str
    data: Optional[str] = None  # base64 или URL


class PerevalSubmitData(BaseModel):
    beauty_title: str
    title: str
    other_titles: Optional[str] = ""
    connect: Optional[str] = ""
    add_time: datetime
    user: User
    coords: Coords
    level: Level
    images: List[Image]