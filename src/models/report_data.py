"""
Model for Salesforce Report Data
"""

from dataclasses import dataclass
from typing import Optional, List, Dict
from datetime import datetime


@dataclass
class ReportData:
    """Model for storing Salesforce report metadata and results"""
    report_id: str
    report_name: str
    report_type: str  # e.g., 'Pipeline', 'Closed Won'
    
    # Report metadata
    run_date: datetime
    filters: Dict[str, any]
    columns: List[str]
    
    # Raw data from report
    raw_data: List[Dict]
    
    # Summary statistics
    total_records: int
    total_amount: float
    grouping_fields: Optional[List[str]] = None
    summary_fields: Optional[List[str]] = None
    
    def to_dict(self) -> Dict:
        """Convert report data to dictionary for CSV export"""
        return {
            'report_id': self.report_id,
            'report_name': self.report_name,
            'report_type': self.report_type,
            'run_date': self.run_date.isoformat(),
            'total_records': self.total_records,
            'total_amount': self.total_amount,
            'filters': str(self.filters),
            'columns': ','.join(self.columns),
            'grouping_fields': ','.join(self.grouping_fields) if self.grouping_fields else None,
            'summary_fields': ','.join(self.summary_fields) if self.summary_fields else None
        } 