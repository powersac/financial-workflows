# Salesforce Data Retrieval Tool

A Python GUI application for retrieving and managing Salesforce data via API integration.

## Project Structure

```
FinanceWorkflows/
│
├── src/
│   ├── models.py      # Data models for Salesforce objects
│   └── main.py        # Main GUI application
│
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Features

- **Modern GUI Interface**: Built with tkinter for cross-platform compatibility
- **Salesforce Connection Management**: Easy connection setup with instance URL
- **Data Models**: Pre-defined models for Accounts, Contacts, and Opportunities
- **Progress Tracking**: Visual progress bar and status updates
- **Threaded Operations**: Non-blocking data retrieval to keep GUI responsive
- **Error Handling**: Comprehensive error handling and user feedback

## Prerequisites

- Python 3.8 or higher
- Active Salesforce account with API access
- Salesforce Connected App (for API integration)

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd /c/Users/Jonathan\ Jackson/Projects/FinanceWorkflows
   ```

2. **Create a virtual environment (recommended)**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the GUI application**:
   ```bash
   python src/main.py
   ```

2. **Using the Application**:
   - Enter your Salesforce instance URL (e.g., `https://your-company.my.salesforce.com`)
   - Click "Connect to Salesforce" to establish connection
   - Once connected, click "Retrieve Salesforce Data" to fetch data
   - Use "Clear Data" to reset the application

## Current Status

This is the **initial setup** with the following completed:

✅ **Completed**:
- Project structure setup
- Data models for Salesforce objects (Account, Contact, Opportunity)
- GUI framework with tkinter
- Connection interface
- Progress tracking and status updates
- Threading for non-blocking operations

🔄 **Next Steps** (to be implemented):
- Salesforce API authentication (OAuth 2.0)
- Actual data retrieval from Salesforce REST API
- Data parsing and model population
- Export functionality
- Configuration management

## Data Models

The application includes pre-defined models for common Salesforce objects:

- **SalesforceConnection**: Manages connection configuration
- **Account**: Salesforce Account records
- **Contact**: Salesforce Contact records  
- **Opportunity**: Salesforce Opportunity records
- **SalesforceDataManager**: Centralized data management

## Configuration

For the next implementation phase, you'll need:

1. **Salesforce Connected App**:
   - Consumer Key (Client ID)
   - Consumer Secret (Client Secret)
   - Callback URL

2. **User Credentials**:
   - Username
   - Password
   - Security Token (if required)

## GUI Features

- **Connection Panel**: Instance URL input and connection status
- **Action Buttons**: Connect, Retrieve Data, Clear Data
- **Progress Tracking**: Visual progress bar with status updates
- **Output Area**: Scrollable text area for logs and results
- **Status Bar**: Real-time status information

## Development Notes

- The GUI is built with tkinter for maximum compatibility
- Threading is used to prevent GUI freezing during operations
- Comprehensive error handling and user feedback
- Modular design for easy extension and maintenance

## Troubleshooting

**Common Issues**:
- Ensure Python 3.8+ is installed
- Check that all dependencies are installed via pip
- Verify Salesforce instance URL format
- Ensure tkinter is available (usually included with Python)

**Support**:
- Check the output area in the GUI for detailed error messages
- Verify your Salesforce credentials and permissions
- Ensure your IP is whitelisted in Salesforce (if applicable)

## Next Development Phase

Ready for Salesforce API integration! The foundation is now in place to add:
- OAuth 2.0 authentication flow
- REST API calls to Salesforce
- Data parsing and model population
- Advanced features like filtering and export 