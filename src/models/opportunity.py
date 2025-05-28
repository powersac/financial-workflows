"""
Salesforce Opportunity model
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Opportunity:
    """Model for Salesforce Opportunity object"""
    id: str
    name: str
    stage_name: str
    amount: Optional[float] = None
    close_date: Optional[datetime] = None
    account_id: Optional[str] = None
    probability: Optional[int] = None
    created_date: Optional[datetime] = None 