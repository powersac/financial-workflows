"""
Salesforce Opportunity model
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class Opportunity:
    """Model for Salesforce Opportunity object"""
    # Basic Information
    id: str
    name: str
    stage_name: str
    amount: Optional[float] = None
    
    # Expected Value Fields
    expected_value: Optional[float] = None
    expected_income: Optional[float] = None
    expected_value_gap: Optional[float] = None  # expected_value - expected_income
    
    # Dates
    close_date: Optional[datetime] = None
    created_date: Optional[datetime] = None
    last_modified_date: Optional[datetime] = None
    fiscal_quarter: Optional[str] = None
    fiscal_year: Optional[str] = None
    
    # Relationships
    account_id: Optional[str] = None
    owner_id: Optional[str] = None
    owner_name: Optional[str] = None
    
    # Classification
    type: Optional[str] = None
    product_line: Optional[str] = None
    region: Optional[str] = None
    
    # Forecasting
    probability: Optional[int] = None
    forecast_category: Optional[str] = None
    
    # Pipeline Tracking
    is_closed: bool = False
    is_won: bool = False
    days_in_stage: Optional[int] = None
    previous_stage: Optional[str] = None
    stage_changes: Optional[List[dict]] = None  # List of stage change events
    
    def to_dict(self) -> dict:
        """Convert opportunity to dictionary for CSV export"""
        return {
            'id': self.id,
            'name': self.name,
            'stage_name': self.stage_name,
            'amount': self.amount,
            'expected_value': self.expected_value,
            'expected_income': self.expected_income,
            'expected_value_gap': self.expected_value_gap,
            'close_date': self.close_date.isoformat() if self.close_date else None,
            'fiscal_quarter': self.fiscal_quarter,
            'fiscal_year': self.fiscal_year,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'last_modified_date': self.last_modified_date.isoformat() if self.last_modified_date else None,
            'account_id': self.account_id,
            'owner_id': self.owner_id,
            'owner_name': self.owner_name,
            'type': self.type,
            'product_line': self.product_line,
            'region': self.region,
            'probability': self.probability,
            'forecast_category': self.forecast_category,
            'is_closed': self.is_closed,
            'is_won': self.is_won,
            'days_in_stage': self.days_in_stage,
            'previous_stage': self.previous_stage
        } 