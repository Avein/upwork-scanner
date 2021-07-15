from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Address:
    line_1: str
    line_2: str
    city: str
    state: str
    postal_code: str
    country: str


@dataclass
class Employment:
    employer_name: str
    position: str
    start_date: str
    end_date: str


@dataclass
class ProfileSettings:
    account: Optional[str]
    employer: List[Employment]
    created_at: Optional[str]
    updated_at: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    birth_date: Optional[str]
    picture_url: Optional[str]
    address: Optional[Address]
    ssn: Optional[str]
    gender: Optional[str]
    metadata: Dict[str, Any]
