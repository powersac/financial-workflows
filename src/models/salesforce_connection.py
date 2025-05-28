"""
Salesforce connection configuration model
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class SalesforceConnection:
    """Model for Salesforce connection configuration"""
    instance_url: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    is_connected: bool = False 