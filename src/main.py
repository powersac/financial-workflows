"""
Main application for Salesforce pipeline analysis
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from simple_salesforce import Salesforce

from src.services.report_service import SalesforceReportService

def get_env_var(key, alt_key=None):
    """Get environment variable with fallback to alternative key"""
    value = os.environ.get(key)
    if value is None and alt_key:
        value = os.environ.get(alt_key)
    return value

def load_env_file(env_path):
    """Load environment variables from file"""
    if not os.path.exists(env_path):
        raise FileNotFoundError(f"Environment file not found at: {env_path}")
    
    print("\nDEBUG: Reading .env file contents:")
    print("-" * 50)
    
    env_vars = {}
    try:
        with open(env_path, 'r', encoding='utf-8-sig') as f:  # Note: using utf-8-sig to handle BOM
            content = f.read()
            print("Raw file content:")
            print(repr(content))
            print("\nProcessing lines:")
            
            for line_num, line in enumerate(content.splitlines(), 1):
                # Remove whitespace and comments
                line = line.strip()
                if not line or line.startswith('#'):
                    print(f"Line {line_num}: Skipping empty or comment line: {repr(line)}")
                    continue
                
                print(f"Processing line {line_num}: {repr(line)}")
                
                if '=' not in line:
                    print(f"Warning: Line {line_num} is not in KEY=VALUE format: {repr(line)}")
                    continue
                
                # Split on first = only
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip("'").strip('"')
                
                if not key:
                    print(f"Warning: Empty key on line {line_num}")
                    continue
                
                if not value:
                    print(f"Warning: Empty value for key {key} on line {line_num}")
                    continue
                
                print(f"Found valid key-value pair: {key}=<value hidden>")
                os.environ[key] = value
                env_vars[key] = value
                
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        raise
    
    print("\nFound environment variables:", list(env_vars.keys()))
    
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
    
    print("-" * 50)
    return credentials

class PipelineAnalyzer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pipeline Analyzer")
        self.root.geometry("800x600")
        
        # Load environment variables from src/.env
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        print(f"\nLooking for .env file at: {env_path}")
        print(f"File exists: {os.path.exists(env_path)}")
        print(f"File size: {os.path.getsize(env_path)} bytes")
        
        try:
            credentials = load_env_file(env_path)
            print("\nEnvironment variables loaded successfully")
            print("Credentials status:")
            print(f"Username present: {bool(credentials.get('username'))}")
            print(f"Password present: {bool(credentials.get('password'))}")
            print(f"Security token present: {bool(credentials.get('security_token'))}")
        except Exception as e:
            print(f"\nError loading environment variables: {str(e)}")
            raise
        
        # Initialize Salesforce connection
        self.sf = Salesforce(
            username=credentials['username'],
            password=credentials['password'],
            security_token=credentials['security_token']
        )
        
        # Initialize services
        self.report_service = SalesforceReportService(self.sf)
        
        # Create UI
        self.create_ui()
    
    def create_ui(self):
        """Create the user interface"""
        # Report ID inputs
        report_frame = ttk.LabelFrame(self.root, text="Report Configuration", padding=10)
        report_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(report_frame, text="Pipeline Report ID:").grid(row=0, column=0, sticky=tk.W)
        self.pipeline_report_id = ttk.Entry(report_frame, width=50)
        self.pipeline_report_id.insert(0, self.report_service.pipeline_report_id)
        self.pipeline_report_id.grid(row=0, column=1, padx=5)
        
        ttk.Label(report_frame, text="Closed Won Report ID:").grid(row=1, column=0, sticky=tk.W)
        self.closed_won_report_id = ttk.Entry(report_frame, width=50)
        self.closed_won_report_id.insert(0, self.report_service.closed_won_report_id)
        self.closed_won_report_id.grid(row=1, column=1, padx=5)
        
        # Output configuration
        output_frame = ttk.LabelFrame(self.root, text="Output Configuration", padding=10)
        output_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(output_frame, text="Output Directory:").grid(row=0, column=0, sticky=tk.W)
        self.output_dir = ttk.Entry(output_frame, width=50)
        self.output_dir.insert(0, "output")
        self.output_dir.grid(row=0, column=1, padx=5)
        
        # Action buttons
        button_frame = ttk.Frame(self.root, padding=10)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(
            button_frame, 
            text="Generate Pipeline Report", 
            command=self.generate_pipeline_report
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Generate Closed Won Report", 
            command=self.generate_closed_won_report
        ).pack(side=tk.LEFT, padx=5)
        
        # Status area
        self.status_text = tk.Text(self.root, height=10, width=80)
        self.status_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
    
    def log_status(self, message: str):
        """Add a message to the status area"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
        self.root.update()
    
    def ensure_output_dir(self) -> str:
        """Ensure output directory exists and return path"""
        output_path = self.output_dir.get()
        os.makedirs(output_path, exist_ok=True)
        return output_path
    
    def generate_pipeline_report(self):
        """Generate pipeline report from Salesforce"""
        try:
            self.log_status("Fetching pipeline report data...")
            report_id = self.pipeline_report_id.get()
            
            # Get report data
            report_data = self.report_service.get_report_data(report_id)
            self.log_status(f"Retrieved {report_data.total_records} opportunities")
            
            # Create snapshot
            snapshot = self.report_service.create_pipeline_snapshot(report_data)
            self.log_status(f"Created pipeline snapshot with total amount: ${snapshot.total_amount:,.2f}")
            
            # Export to CSV
            output_path = self.ensure_output_dir()
            self.report_service.export_to_csv(snapshot, output_path)
            self.log_status(f"Exported pipeline data to {output_path}")
            
            messagebox.showinfo("Success", "Pipeline report generated successfully!")
            
        except Exception as e:
            self.log_status(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to generate pipeline report: {str(e)}")
    
    def generate_closed_won_report(self):
        """Generate closed won report from Salesforce"""
        try:
            self.log_status("Fetching closed won report data...")
            report_id = self.closed_won_report_id.get()
            
            # Get report data
            report_data = self.report_service.get_report_data(report_id)
            self.log_status(f"Retrieved {report_data.total_records} closed won opportunities")
            
            # Create snapshot
            snapshot = self.report_service.create_pipeline_snapshot(report_data)
            self.log_status(f"Created closed won snapshot with total amount: ${snapshot.total_amount:,.2f}")
            
            # Export to CSV
            output_path = self.ensure_output_dir()
            self.report_service.export_to_csv(snapshot, output_path)
            self.log_status(f"Exported closed won data to {output_path}")
            
            messagebox.showinfo("Success", "Closed won report generated successfully!")
            
        except Exception as e:
            self.log_status(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to generate closed won report: {str(e)}")
    
    def run(self):
        """Run the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = PipelineAnalyzer()
    app.run() 