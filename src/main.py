"""
Main application file for Salesforce Data Retrieval GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from typing import Optional
from dotenv import load_dotenv
from simple_salesforce import Salesforce
from config import SalesforceConfig


class SalesforceGUI:
    """Main GUI application for Salesforce data retrieval"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Salesforce Data Retrieval Tool")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Load environment variables
        load_dotenv()
        
        # Get Salesforce configuration
        self.config = SalesforceConfig.get_config()
        
        # Initialize connection
        self.sf: Optional[Salesforce] = None
        
        # Setup GUI components
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the main GUI components"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Salesforce Data Retrieval Tool", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Connection section
        connection_frame = ttk.LabelFrame(main_frame, text="Connection Settings", padding="10")
        connection_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        connection_frame.columnconfigure(1, weight=1)
        
        # Instance URL
        ttk.Label(connection_frame, text="Instance URL:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.instance_url_var = tk.StringVar(value=self.config['instance_url'])
        instance_url_entry = ttk.Entry(connection_frame, textvariable=self.instance_url_var, width=50)
        instance_url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Connection status
        self.connection_status_var = tk.StringVar(value="Not Connected")
        self.status_label = ttk.Label(connection_frame, textvariable=self.connection_status_var, 
                                foreground="red")
        self.status_label.grid(row=0, column=2, sticky=tk.E)
        
        # Action buttons section
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Connect button
        self.connect_btn = ttk.Button(button_frame, text="Connect to Salesforce", 
                                     command=self.connect_to_salesforce)
        self.connect_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Retrieve data button
        self.retrieve_btn = ttk.Button(button_frame, text="Retrieve Salesforce Data", 
                                      command=self.retrieve_salesforce_data, state='disabled')
        self.retrieve_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear data button
        self.clear_btn = ttk.Button(button_frame, text="Clear Data", 
                                   command=self.clear_data, state='disabled')
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Run Pipeline Analysis button
        self.pipeline_btn = ttk.Button(button_frame, text="Run Pipeline Analysis", 
                                      command=self.run_pipeline_analysis, state='disabled')
        self.pipeline_btn.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                           maximum=100, mode='determinate')
        self.progress_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Output section
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10")
        output_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        # Text output area
        self.output_text = scrolledtext.ScrolledText(output_frame, height=15, width=70)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E))
        status_frame.columnconfigure(1, weight=1)
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.grid(row=0, column=0, sticky=tk.W)
        
    def connect_to_salesforce(self):
        """Handle Salesforce connection"""
        try:
            self.update_status("Connecting to Salesforce...")
            self.progress_var.set(25)
            
            # Create connection using credentials from .env
            self.sf = Salesforce(
                username=self.config['username'],
                password=self.config['password'],
                security_token=self.config['security_token'],
                instance_url=self.config['instance_url']
            )
            
            # Test connection with a simple query
            self.sf.query("SELECT Id FROM Account LIMIT 1")
            
            # Update UI
            self.connection_status_var.set("Connected")
            self.status_label.configure(foreground="green")
            self.retrieve_btn.configure(state='normal')
            self.clear_btn.configure(state='normal')
            self.pipeline_btn.configure(state='normal')
            
            self.log_message("✓ Successfully connected to Salesforce")
            self.update_status("Connected - Ready to retrieve data")
            
        except Exception as e:
            self.log_message(f"Connection failed: {str(e)}")
            self.update_status("Connection failed")
            self.progress_var.set(0)
            messagebox.showerror("Connection Error", 
                               "Failed to connect to Salesforce. Please check your credentials in the .env file.")
    
    def retrieve_salesforce_data(self):
        """Handle Salesforce data retrieval"""
        if not self.sf:
            messagebox.showerror("Error", "Not connected to Salesforce")
            return
            
        try:
            self.update_status("Retrieving Salesforce data...")
            self.log_message("Starting data retrieval from Salesforce...")
            
            # Run data retrieval in a separate thread
            thread = threading.Thread(target=self._retrieve_data_thread)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.log_message(f"Data retrieval failed: {str(e)}")
            self.update_status("Data retrieval failed")
            messagebox.showerror("Retrieval Error", f"Failed to retrieve data: {str(e)}")
    
    def _retrieve_data_thread(self):
        """Perform data retrieval in a separate thread"""
        try:
            # Query Accounts
            self.root.after(0, lambda: self.log_message("Querying Accounts..."))
            self.root.after(0, lambda: self.progress_var.set(20))
            
            accounts = self.sf.query("""
                SELECT Id, Name, Type, Industry, BillingCity, BillingCountry 
                FROM Account 
                ORDER BY CreatedDate DESC 
                LIMIT 10
            """)
            
            self.root.after(0, lambda: self.log_message(f"Found {len(accounts['records'])} accounts"))
            self.root.after(0, lambda: self.progress_var.set(40))
            
            # Query Opportunities
            self.root.after(0, lambda: self.log_message("Querying Opportunities..."))
            opportunities = self.sf.query("""
                SELECT Id, Name, StageName, Amount, CloseDate 
                FROM Opportunity 
                WHERE IsClosed = false
                ORDER BY CreatedDate DESC 
                LIMIT 10
            """)
            
            self.root.after(0, lambda: self.log_message(f"Found {len(opportunities['records'])} open opportunities"))
            self.root.after(0, lambda: self.progress_var.set(100))
            
            # Display results
            self.root.after(0, lambda: self._display_results(accounts['records'], opportunities['records']))
            
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"Error in data retrieval: {str(e)}"))
            self.root.after(0, lambda: self.update_status("Data retrieval failed"))
            self.root.after(0, lambda: self.progress_var.set(0))
    
    def _display_results(self, accounts, opportunities):
        """Display the retrieved results"""
        self.log_message("\nAccount Summary:")
        for account in accounts:
            self.log_message("-" * 50)
            self.log_message(f"Name: {account['Name']}")
            self.log_message(f"Type: {account.get('Type', 'N/A')}")
            self.log_message(f"Industry: {account.get('Industry', 'N/A')}")
            self.log_message(f"Location: {account.get('BillingCity', 'N/A')}, {account.get('BillingCountry', 'N/A')}")
        
        self.log_message("\nOpen Opportunities:")
        for opp in opportunities:
            self.log_message("-" * 50)
            self.log_message(f"Name: {opp['Name']}")
            self.log_message(f"Stage: {opp['StageName']}")
            self.log_message(f"Amount: ${opp.get('Amount', 0):,.2f}")
            self.log_message(f"Close Date: {opp['CloseDate']}")
        
        self.update_status("Data retrieval completed")
        self.progress_var.set(0)
    
    def clear_data(self):
        """Clear all data from the output"""
        self.output_text.delete(1.0, tk.END)
        self.log_message("All data cleared.")
        self.update_status("Data cleared - Ready")
    
    def run_pipeline_analysis(self):
        """Handle pipeline analysis"""
        if not self.sf:
            messagebox.showerror("Error", "Not connected to Salesforce")
            return
            
        try:
            self.update_status("Running pipeline analysis...")
            self.log_message("Starting pipeline analysis...")
            
            # Query pipeline data
            pipeline_data = self.sf.query("""
                SELECT StageName, COUNT(Id) RecordCount, SUM(Amount) TotalAmount
                FROM Opportunity 
                WHERE IsClosed = false
                GROUP BY StageName
                ORDER BY StageName
            """)
            
            # Display results
            self.log_message("\nPipeline Analysis Results:")
            self.log_message("-" * 50)
            
            total_amount = 0
            total_deals = 0
            
            for stage in pipeline_data['records']:
                count = int(stage['RecordCount'])
                amount = float(stage.get('TotalAmount', 0))
                total_amount += amount
                total_deals += count
                
                self.log_message(f"Stage: {stage['StageName']}")
                self.log_message(f"Number of Deals: {count}")
                self.log_message(f"Total Value: ${amount:,.2f}")
                self.log_message("-" * 50)
            
            self.log_message(f"\nTotal Pipeline:")
            self.log_message(f"Total Deals: {total_deals}")
            self.log_message(f"Total Value: ${total_amount:,.2f}")
            
            self.update_status("Pipeline analysis completed")
            
        except Exception as e:
            self.log_message(f"Pipeline analysis failed: {str(e)}")
            self.update_status("Pipeline analysis failed")
            messagebox.showerror("Analysis Error", f"Failed to run pipeline analysis: {str(e)}")
    
    def log_message(self, message: str):
        """Add a message to the output text area"""
        self.output_text.insert(tk.END, f"{message}\n")
        self.output_text.see(tk.END)
        
    def update_status(self, status: str):
        """Update the status bar"""
        self.status_var.set(status)
        self.root.update_idletasks()


def main():
    """Main function to start the application"""
    root = tk.Tk()
    app = SalesforceGUI(root)
    
    # Center the window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main() 