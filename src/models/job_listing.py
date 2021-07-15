from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PersonalData:
    pass


@dataclass
class Job:
    title: Optional[str]
    type: Optional[str]
    tier: Optional[str]
    budget: Optional[str]
    duration: Optional[str]
    posted_time: Optional[str]
    location_requirement: Optional[str]
    description: Optional[str]
    skills_required: List[str]

    is_verified: bool


@dataclass
class Profile:
    categories: List[str]
    visibility: Optional[str]
    availability: Optional[str]
    profile_completion: Optional[str]
    available_connections: Optional[str]
