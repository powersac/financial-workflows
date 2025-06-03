# Salesforce Data Retrieval Tool

A Python-based GUI application for retrieving and analyzing Salesforce data.

## Features

- Connect to Salesforce using username-password authentication
- View recent Accounts and their details
- Track open Opportunities
- Analyze sales pipeline by stage
- Real-time data retrieval and display
- Clean and intuitive user interface

## Setup

1. Clone the repository:
```bash
git clone [your-repository-url]
cd FinancialWorkflows
```

2. Install dependencies:
```bash
pip install python-dotenv simple-salesforce
```

3. Configure your Salesforce credentials:
   - Create a `.env` file in the root directory
   - Add your Salesforce credentials:
```
SALESFORCE_INSTANCE_URL=https://your-instance.salesforce.com
SALESFORCE_USERNAME=your.email@example.com
SALESFORCE_PASSWORD=your_password
SALESFORCE_SECURITY_TOKEN=your_security_token
```

## Running the Application

```bash
cd src
python main.py
```

## Project Structure

```
FinancialWorkflows/
├── src/
│   ├── main.py           # Main application file
│   └── config.py         # Configuration management
├── .env                  # Salesforce credentials (not in git)
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## Security Notes

- Never commit your `.env` file to version control
- Keep your security token safe
- Reset your security token if you suspect it's been compromised

## Development

This project uses:
- Python 3.x
- tkinter for the GUI
- simple-salesforce for Salesforce API integration
- python-dotenv for environment variable management

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