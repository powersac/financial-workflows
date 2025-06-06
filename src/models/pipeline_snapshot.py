"""
Pipeline Snapshot model to store point-in-time pipeline data
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict
from .opportunity import Opportunity


@dataclass
class PipelineSnapshot:
    """Model for storing pipeline data at a specific point in time"""
    snapshot_date: datetime
    opportunities: List[Opportunity]
    total_amount: float
    total_count: int
    stage_summary: Dict[str, Dict[str, float]]  # Stage -> {count, amount}
    region_summary: Dict[str, Dict[str, float]]  # Region -> {count, amount}
    owner_summary: Dict[str, Dict[str, float]]   # Owner -> {count, amount}
    
    # Metadata
    report_id: Optional[str] = None
    report_name: Optional[str] = None
    generated_by: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert snapshot to dictionary for CSV export"""
        return {
            'snapshot_date': self.snapshot_date.isoformat(),
            'total_amount': self.total_amount,
            'total_count': self.total_count,
            'report_id': self.report_id,
            'report_name': self.report_name,
            'generated_by': self.generated_by,
            # Add stage summaries
            **{f"stage_{stage}_amount": data['amount'] 
               for stage, data in self.stage_summary.items()},
            **{f"stage_{stage}_count": data['count'] 
               for stage, data in self.stage_summary.items()},
            # Add region summaries
            **{f"region_{region}_amount": data['amount'] 
               for region, data in self.region_summary.items()},
            **{f"region_{region}_count": data['count'] 
               for region, data in self.region_summary.items()},
        } 