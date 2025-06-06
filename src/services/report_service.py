"""
Service for handling Salesforce report data retrieval and processing
"""

from typing import Optional, Dict, List
from datetime import datetime
import pandas as pd
from simple_salesforce import Salesforce

from src.models.report_data import ReportData
from src.models.opportunity import Opportunity
from src.models.pipeline_snapshot import PipelineSnapshot


class SalesforceReportService:
    def __init__(self, sf_connection: Salesforce):
        self.sf = sf_connection
        
        # Default report IDs (can be overridden)
        self.pipeline_report_id = "00OIV000001TKQz2AO"
        self.closed_won_report_id = "00OIV00000MagdZ2AR"
    
    def get_report_metadata(self, report_id: str) -> Dict:
        """Get metadata about a report"""
        return self.sf.restful(f'analytics/reports/{report_id}/describe')
    
    def get_report_data(self, report_id: str) -> ReportData:
        """Get data from a Salesforce report"""
        # Get report details
        metadata = self.get_report_metadata(report_id)
        results = self.sf.restful(f'analytics/reports/{report_id}')
        
        # Extract relevant data
        report_name = metadata['reportMetadata']['name']
        report_type = metadata['reportMetadata']['reportType']['type']
        
        # Process filters
        filters = {
            filter_item['column']: filter_item['value']
            for filter_item in metadata['reportMetadata'].get('reportFilters', [])
        }
        
        # Get columns
        columns = [detail['label'] for detail in metadata['detailColumns']]
        
        # Process factmap data
        raw_data = []
        for key, value in results['factMap'].items():
            if 'rows' in value:
                for row in value['rows']:
                    row_data = {}
                    for i, cell in enumerate(row['dataCells']):
                        row_data[columns[i]] = cell['value']
                    raw_data.append(row_data)
        
        return ReportData(
            report_id=report_id,
            report_name=report_name,
            report_type=report_type,
            run_date=datetime.now(),
            filters=filters,
            columns=columns,
            raw_data=raw_data,
            total_records=len(raw_data),
            total_amount=sum(float(row.get('Amount', 0) or 0) for row in raw_data)
        )
    
    def create_pipeline_snapshot(self, report_data: ReportData, is_pipeline: bool = True) -> PipelineSnapshot:
        """Convert report data into a pipeline snapshot"""
        opportunities = []
        stage_summary = {}
        region_summary = {}
        owner_summary = {}
        
        for row in report_data.raw_data:
            # Handle dates
            close_date = None
            if row.get('Close Date'):
                try:
                    close_date = datetime.strptime(row['Close Date'], '%Y-%m-%d')
                except ValueError:
                    # Try alternate format
                    close_date = datetime.strptime(row['Close Date'], '%m/%d/%Y')
            
            # Extract fiscal period if available
            fiscal_info = row.get('Fiscal Period', '').split(' ')
            fiscal_quarter = fiscal_info[0] if len(fiscal_info) > 0 else None
            fiscal_year = fiscal_info[1] if len(fiscal_info) > 1 else None
            
            # Create Opportunity object with different focus based on report type
            if is_pipeline:
                # For pipeline report, focus on expected values
                expected_value = float(row.get('Expected Value', 0) or 0)
                expected_income = float(row.get('Expected Income', 0) or 0)
                opp = Opportunity(
                    id=row.get('Opportunity ID'),
                    name=row.get('Opportunity Name'),
                    stage_name=row.get('Stage'),
                    amount=float(row.get('Amount', 0) or 0),
                    expected_value=expected_value,
                    expected_income=expected_income,
                    expected_value_gap=expected_value - expected_income,
                    close_date=close_date,
                    fiscal_quarter=fiscal_quarter,
                    fiscal_year=fiscal_year,
                    account_id=row.get('Account ID'),
                    owner_id=row.get('Owner ID'),
                    owner_name=row.get('Owner Name'),
                    type=row.get('Type'),
                    product_line=row.get('Product Line'),
                    region=row.get('Region'),
                    probability=int(row.get('Probability', 0)),
                    forecast_category=row.get('Forecast Category'),
                    is_closed=False,
                    is_won=False
                )
            else:
                # For closed won report, focus on actual amount and timing
                opp = Opportunity(
                    id=row.get('Opportunity ID'),
                    name=row.get('Opportunity Name'),
                    stage_name='Closed Won',
                    amount=float(row.get('Amount', 0) or 0),
                    close_date=close_date,
                    fiscal_quarter=fiscal_quarter,
                    fiscal_year=fiscal_year,
                    account_id=row.get('Account ID'),
                    owner_id=row.get('Owner ID'),
                    owner_name=row.get('Owner Name'),
                    type=row.get('Type'),
                    product_line=row.get('Product Line'),
                    region=row.get('Region'),
                    is_closed=True,
                    is_won=True
                )
            
            opportunities.append(opp)
            
            # Update summaries with appropriate metrics
            def update_summary(summary_dict: Dict, key: str, metrics: Dict[str, float]):
                if key not in summary_dict:
                    summary_dict[key] = {
                        'count': 0,
                        'amount': 0.0,
                        'expected_value': 0.0,
                        'expected_income': 0.0,
                        'expected_value_gap': 0.0
                    }
                summary_dict[key]['count'] += 1
                for metric_name, value in metrics.items():
                    summary_dict[key][metric_name] += value
            
            if is_pipeline:
                metrics = {
                    'amount': opp.amount or 0,
                    'expected_value': opp.expected_value or 0,
                    'expected_income': opp.expected_income or 0,
                    'expected_value_gap': opp.expected_value_gap or 0
                }
            else:
                metrics = {'amount': opp.amount or 0}
            
            update_summary(stage_summary, opp.stage_name, metrics)
            update_summary(region_summary, opp.region or 'Unknown', metrics)
            update_summary(owner_summary, opp.owner_name or 'Unknown', metrics)
        
        return PipelineSnapshot(
            snapshot_date=datetime.now(),
            opportunities=opportunities,
            total_amount=sum(opp.amount or 0 for opp in opportunities),
            total_count=len(opportunities),
            stage_summary=stage_summary,
            region_summary=region_summary,
            owner_summary=owner_summary,
            report_id=report_data.report_id,
            report_name=report_data.report_name
        )
    
    def export_to_csv(self, snapshot: PipelineSnapshot, output_path: str, is_pipeline: bool = True):
        """Export pipeline snapshot to CSV files"""
        # Create timestamp for filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prefix = "pipeline" if is_pipeline else "closed_won"
        
        # Export summary data
        summary_df = pd.DataFrame([snapshot.to_dict()])
        summary_df.to_csv(f"{output_path}/{prefix}_summary_{timestamp}.csv", index=False)
        
        # Export opportunity details
        opps_df = pd.DataFrame([opp.to_dict() for opp in snapshot.opportunities])
        
        # Sort and group by fiscal period if pipeline report
        if is_pipeline:
            opps_df['expected_value_gap'] = opps_df['expected_value'] - opps_df['expected_income']
            opps_df = opps_df.sort_values(['fiscal_year', 'fiscal_quarter', 'expected_value_gap'], 
                                        ascending=[True, True, False])
        else:
            # For closed won, sort by close date and amount
            opps_df = opps_df.sort_values(['close_date', 'amount'], 
                                        ascending=[True, False])
        
        opps_df.to_csv(f"{output_path}/{prefix}_opportunities_{timestamp}.csv", index=False)
        
        # Export stage summary
        stage_df = pd.DataFrame([
            {'stage': stage, **data}
            for stage, data in snapshot.stage_summary.items()
        ])
        stage_df.to_csv(f"{output_path}/{prefix}_stages_{timestamp}.csv", index=False)
        
        # Export region summary
        region_df = pd.DataFrame([
            {'region': region, **data}
            for region, data in snapshot.region_summary.items()
        ])
        region_df.to_csv(f"{output_path}/{prefix}_regions_{timestamp}.csv", index=False)
        
        # Create temporal analysis for closed won
        if not is_pipeline:
            temporal_df = opps_df.groupby(['fiscal_year', 'fiscal_quarter']).\
                agg({
                    'amount': ['sum', 'count'],
                    'id': 'count'
                }).reset_index()
            temporal_df.columns = ['fiscal_year', 'fiscal_quarter', 'total_amount', 
                                 'deal_count', 'opportunity_count']
            temporal_df.to_csv(f"{output_path}/{prefix}_temporal_{timestamp}.csv", index=False) 