"""
Data models for Salesforce integration
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class SalesforceConnection:
    """Model for Salesforce connection configuration"""
    instance_url: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    is_connected: bool = False


@dataclass
class SalesforceRecord:
    """Generic model for Salesforce records"""
    id: str
    object_type: str
    fields: Dict[str, Any]
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None


@dataclass
class Account:
    """Model for Salesforce Account object"""
    id: str
    name: str
    type: Optional[str] = None
    industry: Optional[str] = None
    annual_revenue: Optional[float] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    created_date: Optional[datetime] = None


@dataclass
class Contact:
    """Model for Salesforce Contact object"""
    id: str
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    account_id: Optional[str] = None
    title: Optional[str] = None
    created_date: Optional[datetime] = None


@dataclass
class Opportunity:
    """Model for Salesforce Opportunity object"""
    id: str
    name: str
    stage_name: str
    amount: Optional[float] = None
    close_date: Optional[datetime] = None
    account_id: Optional[str] = None
    probability: Optional[int] = None
    created_date: Optional[datetime] = None


class SalesforceDataManager:
    """Manager class for handling Salesforce data operations"""
    
    def __init__(self):
        self.connection: Optional[SalesforceConnection] = None
        self.accounts: List[Account] = []
        self.contacts: List[Contact] = []
        self.opportunities: List[Opportunity] = []
    
    def set_connection(self, connection: SalesforceConnection):
        """Set the Salesforce connection"""
        self.connection = connection
    
    def clear_data(self):
        """Clear all loaded data"""
        self.accounts.clear()
        self.contacts.clear()
        self.opportunities.clear()
    
    def add_accounts(self, accounts: List[Account]):
        """Add accounts to the manager"""
        self.accounts.extend(accounts)
    
    def add_contacts(self, contacts: List[Contact]):
        """Add contacts to the manager"""
        self.contacts.extend(contacts)
    
    def add_opportunities(self, opportunities: List[Opportunity]):
        """Add opportunities to the manager"""
        self.opportunities.extend(opportunities)
    
    def get_account_by_id(self, account_id: str) -> Optional[Account]:
        """Get account by ID"""
        return next((acc for acc in self.accounts if acc.id == account_id), None)
    
    def get_contacts_by_account(self, account_id: str) -> List[Contact]:
        """Get all contacts for a specific account"""
        return [contact for contact in self.contacts if contact.account_id == account_id]
    
    def get_opportunities_by_account(self, account_id: str) -> List[Opportunity]:
        """Get all opportunities for a specific account"""
        return [opp for opp in self.opportunities if opp.account_id == account_id]
    
    def create_account_opportunity_mapping(self) -> Dict[str, List[Opportunity]]:
        """
        Create a dictionary mapping account IDs to their associated opportunities
        
        Returns:
            Dict[str, List[Opportunity]]: Dictionary with account IDs as keys 
                                        and lists of opportunities as values
        """
        account_opportunity_map = {}
        
        # Loop over all known accounts
        for account in self.accounts:
            # Get all opportunities for this account
            account_opportunities = self.get_opportunities_by_account(account.id)
            account_opportunity_map[account.id] = account_opportunities
        
        return account_opportunity_map
    
    def create_account_object_opportunity_mapping(self) -> Dict[Account, List[Opportunity]]:
        """
        Create a dictionary mapping Account objects to their associated opportunities
        
        Returns:
            Dict[Account, List[Opportunity]]: Dictionary with Account objects as keys 
                                            and lists of opportunities as values
        """
        account_opportunity_map = {}
        
        # Loop over all known accounts
        for account in self.accounts:
            # Get all opportunities for this account
            account_opportunities = self.get_opportunities_by_account(account.id)
            account_opportunity_map[account] = account_opportunities
        
        return account_opportunity_map
    
    def get_account_opportunity_summary(self) -> Dict[str, Dict[str, Any]]:
        """
        Create a comprehensive summary mapping accounts to opportunity metrics
        
        Returns:
            Dict[str, Dict[str, Any]]: Dictionary with account IDs as keys and 
                                     opportunity summary data as values
        """
        summary = {}
        
        # Loop over all known accounts
        for account in self.accounts:
            opportunities = self.get_opportunities_by_account(account.id)
            
            # Calculate metrics for this account
            total_opportunities = len(opportunities)
            total_amount = sum(opp.amount or 0 for opp in opportunities)
            avg_amount = total_amount / total_opportunities if total_opportunities > 0 else 0
            
            # Group by stage
            stages = {}
            for opp in opportunities:
                stage = opp.stage_name
                if stage not in stages:
                    stages[stage] = {'count': 0, 'total_amount': 0}
                stages[stage]['count'] += 1
                stages[stage]['total_amount'] += opp.amount or 0
            
            summary[account.id] = {
                'account_name': account.name,
                'account_object': account,
                'opportunities': opportunities,
                'total_opportunities': total_opportunities,
                'total_amount': total_amount,
                'average_amount': avg_amount,
                'stages': stages
            }
        
        return summary 