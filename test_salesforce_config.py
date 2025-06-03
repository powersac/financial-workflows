"""
Test script to verify Salesforce configuration
"""
import os
from dotenv import load_dotenv
from simple_salesforce import Salesforce
from config import SalesforceConfig

def test_connection():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get configuration
    config = SalesforceConfig.get_config()
    
    print("Testing Salesforce connection...")
    print(f"Instance URL: {config['instance_url']}")
    print(f"Username: {config['username']}")
    
    # Debug information (safely)
    print("\nCredential Check:")
    print(f"Username is set: {'Yes' if config['username'] else 'No'}")
    print(f"Password is set: {'Yes' if config['password'] else 'No'}")
    print(f"Security Token is set: {'Yes' if config['security_token'] else 'No'}")
    print(f"Username length: {len(config['username']) if config['username'] else 0}")
    print(f"Password length: {len(config['password']) if config['password'] else 0}")
    print(f"Security Token length: {len(config['security_token']) if config['security_token'] else 0}")
    
    try:
        # Attempt to connect to Salesforce
        sf = Salesforce(
            username=config['username'],
            password=config['password'],
            security_token=config['security_token'],
            instance_url=config['instance_url']
        )
        
        # Try a simple query to verify connection
        result = sf.query("SELECT Id, Name FROM Account LIMIT 1")
        
        print("\n✅ Connection successful!")
        print(f"Successfully connected to Salesforce org: {sf.sf_instance}")
        print(f"API Version: {sf.sf_version}")
        print("\nTest query result:")
        if result['records']:
            print(f"Found account: {result['records'][0]['Name']}")
        else:
            print("No accounts found (but connection is working)")
            
    except Exception as e:
        print("\n❌ Connection failed!")
        print(f"Error: {str(e)}")
        print("\nPlease verify your credentials in the .env file:")
        print("1. Check that your username is correct")
        print("2. Verify your password")
        print("3. Make sure your security token is correct")
        print("4. Confirm the instance URL is correct")

if __name__ == "__main__":
    test_connection() 