"""
Test script to query Salesforce data
"""
import os
from dotenv import load_dotenv
from simple_salesforce import Salesforce
from config import SalesforceConfig

def test_salesforce_query():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get configuration
    config = SalesforceConfig.get_config()
    
    print("Connecting to Salesforce...")
    print(f"Instance URL: {config['instance_url']}")
    print(f"Username: {config['username']}")
    
    try:
        # Connect to Salesforce
        sf = Salesforce(
            username=config['username'],
            password=config['password'],
            security_token=config['security_token'],
            instance_url=config['instance_url']
        )
        
        print("\n✅ Connection successful!")
        print(f"Connected to Salesforce org: {sf.sf_instance}")
        
        # Query Accounts
        print("\nQuerying Accounts...")
        result = sf.query("""
            SELECT Id, Name, Type, Industry, BillingCity, BillingCountry 
            FROM Account 
            ORDER BY CreatedDate DESC 
            LIMIT 5
        """)
        
        if result['records']:
            print(f"\nFound {len(result['records'])} accounts:")
            print("-" * 50)
            for account in result['records']:
                print(f"Name: {account['Name']}")
                print(f"Type: {account.get('Type', 'N/A')}")
                print(f"Industry: {account.get('Industry', 'N/A')}")
                print(f"Location: {account.get('BillingCity', 'N/A')}, {account.get('BillingCountry', 'N/A')}")
                print("-" * 50)
        else:
            print("No accounts found.")
            
        # Query Opportunities
        print("\nQuerying Recent Opportunities...")
        opp_result = sf.query("""
            SELECT Id, Name, StageName, Amount, CloseDate 
            FROM Opportunity 
            WHERE IsClosed = false
            ORDER BY CreatedDate DESC 
            LIMIT 5
        """)
        
        if opp_result['records']:
            print(f"\nFound {len(opp_result['records'])} open opportunities:")
            print("-" * 50)
            for opp in opp_result['records']:
                print(f"Name: {opp['Name']}")
                print(f"Stage: {opp['StageName']}")
                print(f"Amount: ${opp.get('Amount', 0):,.2f}")
                print(f"Close Date: {opp['CloseDate']}")
                print("-" * 50)
        else:
            print("No open opportunities found.")
            
    except Exception as e:
        print("\n❌ Error occurred!")
        print(f"Error: {str(e)}")
        print("\nPlease verify your credentials in the .env file:")
        print("1. Check that your username is correct")
        print("2. Verify your password")
        print("3. Make sure your security token is correct")
        print("4. Confirm the instance URL is correct")

if __name__ == "__main__":
    test_salesforce_query() 