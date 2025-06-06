"""
Salesforce data models package

This package contains all the data models for Salesforce integration.
"""

# Import all models for convenient access
from .salesforce_connection import SalesforceConnection
from .salesforce_record import SalesforceRecord
from .account import Account
from .contact import Contact
from .opportunity import Opportunity

__all__ = [
    'SalesforceConnection',
    'SalesforceRecord',
    'Account',
    'Contact',
    'Opportunity'
]

"""
Models package initialization
""" 