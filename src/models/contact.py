"""
Salesforce Contact model
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Contact:
    """Model for Salesforce Contact object"""
    id: str
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    account_id: Optional[str] = None
    title: Optional[str] = None
    created_date: Optional[datetime] = None 