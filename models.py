from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    uid: str
    user_name: str
    title: str
    linkedin_profile_url: Optional[str] = None
    linkedin_image_url: Optional[str] = None
    location: str
    req_school: str
    req_country: str
    source_category: str  # "schools_only", "salesnav_only", "both"
    color_class: str  # Bootstrap color class

class UserDetail(BaseModel):
    uid: str
    user_name: str
    title: str
    linkedin_profile_url: Optional[str] = None
    linkedin_image_url: Optional[str] = None
    location: str
    req_school: str
    req_country: str
    about: Optional[str] = None
    headline: Optional[str] = None
    skills: Optional[str] = None
    experience: Optional[str] = None
    in_schools_table: bool
    in_salesnav_table: bool
    schools_timestamp: Optional[str] = None
    salesnav_timestamp: Optional[str] = None

class FilterParams(BaseModel):
    search: Optional[str] = None
    location_filter: Optional[str] = None
    school_filter: Optional[str] = None
    country_filter: Optional[str] = None
    source_filter: Optional[str] = None
    order_by: str = "user_name"
    order_direction: str = "ASC"
