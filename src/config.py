"""
Salesforce configuration settings
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

class SalesforceConfig:
    @staticmethod
    def get_config() -> Dict[str, Any]:
        """
        Get Salesforce configuration settings.
        Prioritizes environment variables over hardcoded values.
        """
        # Make sure we can find the .env file one directory up
        dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        load_dotenv(dotenv_path)
        
        return {
            # OAuth 2.0 settings
            'client_id': os.getenv('SALESFORCE_CLIENT_ID', ''),
            'client_secret': os.getenv('SALESFORCE_CLIENT_SECRET', ''),
            'redirect_uri': os.getenv('SALESFORCE_REDIRECT_URI', 'http://localhost:8080/callback'),
            
            # Username-Password flow settings
            'username': os.getenv('SALESFORCE_USERNAME', ''),
            'password': os.getenv('SALESFORCE_PASSWORD', ''),
            'security_token': os.getenv('SALESFORCE_SECURITY_TOKEN', ''),
            
            # Instance URL (e.g., https://yourorg.my.salesforce.com)
            'instance_url': os.getenv('SALESFORCE_INSTANCE_URL', ''),
        } 