"""
Generic Salesforce record model
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime


@dataclass
class SalesforceRecord:
    """Generic model for Salesforce records"""
    id: str
    object_type: str
    fields: Dict[str, Any]
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None 