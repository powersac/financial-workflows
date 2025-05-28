"""
Main application file for Salesforce Data Retrieval GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from typing import Optional
from models import SalesforceConnection
from salesforce_data_manager import SalesforceDataManager


class SalesforceGUI:
    """Main GUI application for Salesforce data retrieval"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Salesforce Data Retrieval Tool")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize data manager
        self.data_manager = SalesforceDataManager()
        
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
        self.instance_url_var = tk.StringVar(value="https://your-instance.salesforce.com")
        instance_url_entry = ttk.Entry(connection_frame, textvariable=self.instance_url_var, width=50)
        instance_url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Connection status
        self.connection_status_var = tk.StringVar(value="Not Connected")
        status_label = ttk.Label(connection_frame, textvariable=self.connection_status_var, 
                                foreground="red")
        status_label.grid(row=0, column=2, sticky=tk.E)
        
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
        
    def log_message(self, message: str):
        """Add a message to the output text area"""
        self.output_text.insert(tk.END, f"{message}\n")
        self.output_text.see(tk.END)
        
    def update_status(self, status: str):
        """Update the status bar"""
        self.status_var.set(status)
        self.root.update_idletasks()
        
    def connect_to_salesforce(self):
        """Handle Salesforce connection"""
        try:
            self.update_status("Connecting to Salesforce...")
            self.progress_var.set(25)
            
            instance_url = self.instance_url_var.get().strip()
            if not instance_url:
                messagebox.showerror("Error", "Please enter a valid instance URL")
                return
            
            # Create connection object (authentication will be implemented later)
            connection = SalesforceConnection(instance_url=instance_url)
            self.data_manager.set_connection(connection)
            
            # Simulate connection process
            self.root.after(1000, self._complete_connection)
            
        except Exception as e:
            self.log_message(f"Connection failed: {str(e)}")
            self.update_status("Connection failed")
            self.progress_var.set(0)
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
    
    def _complete_connection(self):
        """Complete the connection process"""
        self.progress_var.set(100)
        self.connection_status_var.set("Connected")
        
        # Update connection status colors
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.LabelFrame):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, ttk.Label) and "Connected" in str(grandchild.cget('text')):
                                grandchild.configure(foreground="green")
        
        # Enable buttons
        self.retrieve_btn.configure(state='normal')
        self.clear_btn.configure(state='normal')
        self.pipeline_btn.configure(state='normal')
        
        self.log_message("✓ Successfully connected to Salesforce")
        self.log_message("Ready to retrieve data. Click 'Retrieve Salesforce Data' to begin.")
        self.update_status("Connected - Ready to retrieve data")
        self.progress_var.set(0)
    
    def retrieve_salesforce_data(self):
        """Handle Salesforce data retrieval"""
        try:
            self.update_status("Retrieving Salesforce data...")
            self.log_message("Starting data retrieval from Salesforce...")
            
            # Run data retrieval in a separate thread to prevent GUI freezing
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
            # Simulate data retrieval steps
            steps = [
                ("Authenticating with Salesforce API...", 20),
                ("Retrieving Account data...", 40),
                ("Retrieving Contact data...", 60),
                ("Retrieving Opportunity data...", 80),
                ("Processing retrieved data...", 100)
            ]
            
            for message, progress in steps:
                self.root.after(0, lambda msg=message: self.log_message(msg))
                self.root.after(0, lambda p=progress: self.progress_var.set(p))
                self.root.after(0, lambda msg=message: self.update_status(msg))
                threading.Event().wait(1)  # Simulate processing time
            
            # Simulate successful data retrieval
            self.root.after(0, self._complete_data_retrieval)
            
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"Error in data retrieval: {str(e)}"))
            self.root.after(0, lambda: self.update_status("Data retrieval failed"))
            self.root.after(0, lambda: self.progress_var.set(0))
    
    def _complete_data_retrieval(self):
        """Complete the data retrieval process"""
        self.log_message("✓ Data retrieval completed successfully!")
        self.log_message("Summary:")
        self.log_message("  - Accounts: 0 (API integration pending)")
        self.log_message("  - Contacts: 0 (API integration pending)")
        self.log_message("  - Opportunities: 0 (API integration pending)")
        self.log_message("\nNote: Actual Salesforce API integration will be implemented in the next step.")
        
        self.update_status("Data retrieval completed")
        self.progress_var.set(0)
    
    def clear_data(self):
        """Clear all data from the manager and output"""
        self.data_manager.clear_data()
        self.output_text.delete(1.0, tk.END)
        self.log_message("All data cleared.")
        self.update_status("Data cleared - Ready")
    
    def run_pipeline_analysis(self):
        """Handle pipeline analysis - function ready for your implementation"""
        try:
            self.update_status("Running pipeline analysis...")
            self.log_message("Starting pipeline analysis...")
            
            # TODO: Add your pipeline analysis logic here
            # This is where you can implement your specific pipeline analysis functionality
            
            # Example structure - replace with your actual implementation:
            self.log_message("Pipeline Analysis Steps:")
            self.log_message("1. [TODO] Analyze opportunity pipeline data")
            self.log_message("2. [TODO] Calculate conversion rates")
            self.log_message("3. [TODO] Generate forecasting metrics")
            self.log_message("4. [TODO] Identify bottlenecks")
            self.log_message("5. [TODO] Create recommendations")
            
            # You can access the retrieved Salesforce data through:
            # - self.data_manager.accounts
            # - self.data_manager.contacts  
            # - self.data_manager.opportunities
            
            # Example of checking available data:
            num_accounts = len(self.data_manager.accounts)
            num_contacts = len(self.data_manager.contacts)
            num_opportunities = len(self.data_manager.opportunities)
            
            self.log_message(f"\nAvailable data for analysis:")
            self.log_message(f"  - Accounts: {num_accounts}")
            self.log_message(f"  - Contacts: {num_contacts}")
            self.log_message(f"  - Opportunities: {num_opportunities}")
            
            if num_opportunities == 0:
                self.log_message("\nNote: No opportunity data available. Run 'Retrieve Salesforce Data' first.")
            else:
                self.log_message("\n✓ Pipeline analysis framework ready!")
                self.log_message("TODO: Implement your specific analysis logic in the run_pipeline_analysis() function.")
            
            self.update_status("Pipeline analysis completed")
            
        except Exception as e:
            self.log_message(f"Pipeline analysis failed: {str(e)}")
            self.update_status("Pipeline analysis failed")
            messagebox.showerror("Analysis Error", f"Failed to run pipeline analysis: {str(e)}")


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