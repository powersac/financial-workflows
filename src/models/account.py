"""
Salesforce Account model
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Account:
    """Model for Salesforce Account object"""
    id: str
    name: str
    type: Optional[str] = None
    industry: Optional[str] = None
    annual_revenue: Optional[float] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    created_date: Optional[datetime] = None 