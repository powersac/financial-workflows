"""
Pipeline Report Generator

This script connects to Salesforce and generates pipeline reports focusing on:
1. Current pipeline with Expected Value vs Expected Income
2. Closed Won opportunities with temporal analysis
"""

import os
from datetime import datetime
from simple_salesforce import Salesforce
import pandas as pd
import json

def get_env_var(key, alt_key=None):
    """Get environment variable with fallback to alternative key"""
    value = os.environ.get(key)
    if value is None and alt_key:
        value = os.environ.get(alt_key)
    return value

def load_credentials(env_path):
    """Load Salesforce credentials from .env file"""
    if not os.path.exists(env_path):
        raise FileNotFoundError(f"Environment file not found at: {env_path}")
    
    with open(env_path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip().strip("'").strip('"')
    
    # Get credentials with fallbacks
    credentials = {
        'username': get_env_var('SF_USERNAME', 'SALESFORCE_USERNAME'),
        'password': get_env_var('SF_PASSWORD', 'SALESFORCE_PASSWORD'),
        'security_token': get_env_var('SF_SECURITY_TOKEN', 'SALESFORCE_SECURITY_TOKEN')
    }
    
    # Verify required variables
    missing_vars = [k for k, v in credentials.items() if v is None]
    if missing_vars:
        raise ValueError(f"Missing required credentials: {', '.join(missing_vars)}")
    
    return credentials

def extract_amount(value):
    """Extract amount from various formats"""
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, dict):
        # Directly return the amount value since currency is always None
        return value['amount']
    if isinstance(value, str):
        # Remove currency symbols and commas
        clean_value = value.replace('$', '').replace(',', '')
        try:
            return float(clean_value)
        except ValueError:
            return None
    return None

def get_report_data(sf, report_id):
    """Get data from a Salesforce report"""
    print(f"Getting report metadata for ID: {report_id}")
    metadata = sf.restful(f'analytics/reports/{report_id}/describe')
    print("Got metadata, fetching results...")
    results = sf.restful(f'analytics/reports/{report_id}')
    
    # Debug information
    print("\nAPI Response Info:")
    print("Metadata keys:", list(metadata.keys()))
    print("Results keys:", list(results.keys()))
    
    # Get columns from report metadata
    columns = []
    if 'reportMetadata' in metadata:
        if isinstance(metadata['reportMetadata']['detailColumns'], list):
            columns = metadata['reportMetadata']['detailColumns']
    
    if not columns and 'reportMetadata' in results:
        if isinstance(results['reportMetadata']['detailColumns'], list):
            columns = results['reportMetadata']['detailColumns']
    
    print(f"\nFound columns: {columns}")
    
    # Process rows
    rows = []
    if 'factMap' in results:
        for key, value in results['factMap'].items():
            if 'rows' in value:
                for row in value['rows']:
                    row_data = {}
                    for i, cell in enumerate(row['dataCells']):
                        col_name = columns[i] if i < len(columns) else f"Column_{i}"
                        row_data[col_name] = cell['value']
                    rows.append(row_data)
    
    df = pd.DataFrame(rows)
    print(f"\nDataFrame Info:")
    print(df.info())
    print("\nSample Data:")
    print(df.head())
    
    return df

def process_pipeline_data(df):
    """Process pipeline opportunities data"""
    print("\nProcessing DataFrame:")
    print("Original columns:", list(df.columns))
    
    # Convert amount fields to numeric
    amount_fields = [
        'AMOUNT', 
        'Opportunity.Services_EV__c',
        'Opportunity.Expected_Value_Minus_Income__c',
        'Opportunity.Interdivision_Expense_Income__c',
        'Opportunity.Expected_Monthly_Recurring_Revenue_MRR__c'
    ]
    
    for field in amount_fields:
        if field in df.columns:
            print(f"Converting {field} to numeric")
            df[field] = df[field].apply(extract_amount)
            df[field] = pd.to_numeric(df[field], errors='coerce')
    
    # Calculate Expected Value Gap if not already present
    if 'Opportunity.Expected_Value_Minus_Income__c' not in df.columns:
        if 'Opportunity.Services_EV__c' in df.columns and 'Opportunity.Interdivision_Expense_Income__c' in df.columns:
            print("Calculating Expected Value Gap")
            df['Expected Value Gap'] = df['Opportunity.Services_EV__c'] - df['Opportunity.Interdivision_Expense_Income__c']
        else:
            print("\nExpected Value Analysis:")
            print("Services EV:", df['Opportunity.Services_EV__c'].sum())
            print("Interdivision Expense Income:", df['Opportunity.Interdivision_Expense_Income__c'].sum())
            print("Calculated Gap:", df['Opportunity.Services_EV__c'].sum() - df['Opportunity.Interdivision_Expense_Income__c'].sum())
            print("Salesforce Gap:", df['Opportunity.Expected_Value_Minus_Income__c'].sum())
    else:
        print("\nExpected Value Analysis:")
        print("Services EV:", df['Opportunity.Services_EV__c'].sum())
        print("Interdivision Expense Income:", df['Opportunity.Interdivision_Expense_Income__c'].sum())
        print("Calculated Gap:", df['Opportunity.Services_EV__c'].sum() - df['Opportunity.Interdivision_Expense_Income__c'].sum())
        print("Salesforce Gap:", df['Opportunity.Expected_Value_Minus_Income__c'].sum())
    
    # Extract close date components if available
    if 'CLOSE_DATE' in df.columns:
        print("Processing close date")
        df['CLOSE_DATE'] = pd.to_datetime(df['CLOSE_DATE'])
        df['Fiscal Year'] = df['CLOSE_DATE'].dt.year
        df['Fiscal Quarter'] = 'Q' + df['CLOSE_DATE'].dt.quarter.astype(str)
    
    print("\nProcessed columns:", list(df.columns))
    return df

def main():
    # Configuration
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    output_dir = 'output'
    pipeline_report_id = "00OIV000001TKQz2AO"
    closed_won_report_id = "00OIV00000MagdZ2AR"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load credentials and connect to Salesforce
    print("Loading credentials...")
    credentials = load_credentials(env_path)
    sf = Salesforce(
        username=credentials['username'],
        password=credentials['password'],
        security_token=credentials['security_token']
    )
    print("Connected to Salesforce successfully")
    
    # Generate timestamp for filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        # Get pipeline data
        print("\nFetching pipeline report...")
        pipeline_df = get_report_data(sf, pipeline_report_id)
        pipeline_df = process_pipeline_data(pipeline_df)
        
        # Save pipeline data
        pipeline_file = f"{output_dir}/pipeline_{timestamp}.csv"
        pipeline_df.to_csv(pipeline_file, index=False)
        print(f"Pipeline data saved to: {pipeline_file}")
        
        # Print summary
        print("\nPipeline Summary:")
        print(f"Total Opportunities: {len(pipeline_df)}")
        if 'AMOUNT' in pipeline_df.columns:
            print(f"Total Amount: ${pipeline_df['AMOUNT'].sum():,.2f}")
        
        print("\nExpected Value Details:")
        if 'Opportunity.Services_EV__c' in pipeline_df.columns:
            print(f"Total Services EV: ${pipeline_df['Opportunity.Services_EV__c'].sum():,.2f}")
        if 'Opportunity.Interdivision_Expense_Income__c' in pipeline_df.columns:
            print(f"Total Interdivision Expense Income: ${pipeline_df['Opportunity.Interdivision_Expense_Income__c'].sum():,.2f}")
        if 'Expected Value Gap' in pipeline_df.columns:
            print(f"Calculated Expected Value Gap: ${pipeline_df['Expected Value Gap'].sum():,.2f}")
        if 'Opportunity.Expected_Value_Minus_Income__c' in pipeline_df.columns:
            print(f"Salesforce Expected Value Gap: ${pipeline_df['Opportunity.Expected_Value_Minus_Income__c'].sum():,.2f}")
        
        # Get closed won data
        print("\nFetching closed won report...")
        closed_won_df = get_report_data(sf, closed_won_report_id)
        closed_won_df = process_pipeline_data(closed_won_df)
        
        # Save closed won data
        closed_won_file = f"{output_dir}/closed_won_{timestamp}.csv"
        closed_won_df.to_csv(closed_won_file, index=False)
        print(f"Closed won data saved to: {closed_won_file}")
        
        # Print summary
        print("\nClosed Won Summary:")
        print(f"Total Opportunities: {len(closed_won_df)}")
        if 'AMOUNT' in closed_won_df.columns:
            print(f"Total Amount: ${closed_won_df['AMOUNT'].sum():,.2f}")
        
        # Create temporal analysis for closed won
        if 'Fiscal Year' in closed_won_df.columns and 'Fiscal Quarter' in closed_won_df.columns:
            temporal = closed_won_df.groupby(['Fiscal Year', 'Fiscal Quarter']).agg({
                'AMOUNT': ['sum', 'count']
            }).reset_index()
            temporal.columns = ['Fiscal Year', 'Fiscal Quarter', 'Total Amount', 'Deal Count']
            
            temporal_file = f"{output_dir}/closed_won_temporal_{timestamp}.csv"
            temporal.to_csv(temporal_file, index=False)
            print(f"\nTemporal analysis saved to: {temporal_file}")
            
            # Print temporal summary
            print("\nTemporal Summary:")
            print(temporal.sort_values(['Fiscal Year', 'Fiscal Quarter']).to_string(index=False))
    
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nFull error details:")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main() 