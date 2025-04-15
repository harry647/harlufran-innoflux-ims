# inventory.py

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from store_logic import StoreLogic
from lab_logic import LabLogic
import os
import shutil
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import re
import logging
import sys

# Dynamic paths for logging and database
def get_app_data_dir():
    return os.path.join(os.getenv("APPDATA", os.path.expanduser("~")), "InventoryManagementSystem")

def get_log_file():
    log_dir = os.path.join(get_app_data_dir(), "logs")
    os.makedirs(log_dir, exist_ok=True)
    return os.path.join(log_dir, "inventory_app.log")

def get_db_path():
    db_dir = get_app_data_dir()
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, "inventory.db")
    if getattr(sys, 'frozen', False) and not os.path.exists(db_path):
        bundled_db = os.path.join(sys._MEIPASS, "inventory.db")
        if os.path.exists(bundled_db):
            shutil.copy2(bundled_db, db_path)
    return db_path

# Configure logging
logging.basicConfig(
    filename=get_log_file(),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Hardcoded admin password
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "harry20070465"

def init_db():
    db_path = get_db_path()
    # Uncomment to reset database on each run (optional)
    # if os.path.exists(db_path):
    #     os.remove(db_path)
    #     print(f"Deleted existing database at {db_path}")

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS items 
                 (id INTEGER PRIMARY KEY, 
                  name TEXT, 
                  category TEXT, 
                  quantity TEXT, 
                  reorder_level TEXT DEFAULT '0', 
                  section TEXT, 
                  subject TEXT DEFAULT NULL, 
                  last_updated TEXT, 
                  expiry_date TEXT DEFAULT NULL, 
                  purchase_unit TEXT DEFAULT 'unit', 
                  molarity REAL DEFAULT NULL, 
                  calories REAL DEFAULT 0.0, 
                  protein REAL DEFAULT 0.0, 
                  CHECK (section = 'lab' OR subject IS NULL))''')

    c.execute('''CREATE TABLE IF NOT EXISTS issuance 
                 (id INTEGER PRIMARY KEY, 
                  item_id INTEGER, 
                  person_name TEXT, 
                  quantity_issued TEXT, 
                  issue_date TEXT, 
                  FOREIGN KEY(item_id) REFERENCES items(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS broken_items 
                 (id INTEGER PRIMARY KEY, 
                  student_id TEXT, 
                  student_name TEXT, 
                  item_id INTEGER, 
                  item_name TEXT, 
                  report_date TEXT, 
                  status TEXT DEFAULT 'Pending', 
                  FOREIGN KEY(item_id) REFERENCES items(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS history 
                 (id INTEGER PRIMARY KEY, 
                  action TEXT, 
                  item_id INTEGER, 
                  details TEXT, 
                  timestamp TEXT, 
                  FOREIGN KEY(item_id) REFERENCES items(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, 
                  username TEXT UNIQUE, 
                  password TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS practical_reports 
                 (id INTEGER PRIMARY KEY, 
                  subject TEXT, 
                  form TEXT, 
                  num_students INTEGER, 
                  topic TEXT, 
                  subtopic TEXT, 
                  time TEXT, 
                  status TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS prices 
                 (item_id INTEGER, 
                  price REAL, 
                  last_updated TEXT, 
                  FOREIGN KEY(item_id) REFERENCES items(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS invoices 
                 (id INTEGER PRIMARY KEY, 
                  supplier TEXT, 
                  item_id INTEGER, 
                  quantity TEXT, 
                  price REAL, 
                  invoice_date TEXT, 
                  FOREIGN KEY(item_id) REFERENCES items(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS meal_templates 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT, 
                  requirements TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS batches 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  item_id INTEGER, 
                  batch_number TEXT, 
                  quantity TEXT, 
                  unit_cost REAL, 
                  received_date TEXT, 
                  expiry_date TEXT, 
                  FOREIGN KEY(item_id) REFERENCES items(id))''')

    c.execute("SELECT COUNT(*) FROM users WHERE username=?", (DEFAULT_ADMIN_USERNAME,))
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                  (DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD))

    
    conn.commit()
    conn.close()
    #print(f"Database initialized at {db_path} with sample data mimicking user actions.")


init_db()

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("1200x800")
        self.logged_in = False
        self.tooltip = None
        self.get_db_path = get_db_path

        # Color scheme for frames
        self.welcome_bg = "#e0f7fa"
        self.login_bg = "#f3e5f5"
        self.store_bg = "#e8f5e9"
        self.lab_bg = "#e3f2fd"
        self.analysis_bg = "#fff3e0"
        self.history_bg = "#f1f8e9"
        self.settings_bg = "#fce4ec"
        
        self.welcome_color_main = "#00838f"
        self.welcome_color_separator = "#4dd0e1"
        self.welcome_font_main = ("Arial Black", 32)
        self.welcome_font_separator = ("Arial", 12, "bold")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_themes()

        self.notification_enabled = True
        self.theme = "clam"
        self.unit_conversions = {
            "mL": {"L": 0.001, "mL": 1},
            "L": {"mL": 1000, "L": 1},
            "units": {"units": 1}
        }

        self.show_login()

    def configure_themes(self):
        # Update base style with frame-specific backgrounds
        self.style.configure("TLabel", font=("Helvetica", 10))
        
        # Button style (unchanged)
        self.style.configure("Appealing.TButton",
                            font=("Segoe UI", 11, "bold"),
                            background="#4CAF50",
                            foreground="white",
                            padding=8,
                            relief="raised")
        self.style.map("Appealing.TButton",
                      background=[("active", "#45a049"), ("disabled", "#a8a8a8")],
                      foreground=[("disabled", "#696969")])

        # Notebook tabs
        self.style.configure("TNotebook.Tab", font=("Helvetica", 10), foreground="black")
        self.style.map("TNotebook.Tab",
                      background=[("selected", "#bbdefb")],
                      foreground=[("selected", "black")])

        self.style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
        self.style.configure("TLabelframe", font=("Helvetica", 10, "bold"), borderwidth=2)
        self.style.configure("TLabelframe.Label", font=("Helvetica", 10))
        self.root.option_add("*TButton", {"style": "Appealing.TButton"})

    def show_login(self):
        self.login_frame = ttk.Frame(self.root, style="TFrame")
        self.login_frame.pack(expand=1, fill="both", padx=10, pady=5)
        self.login_frame.configure(style="Login.TFrame")
        self.style.configure("Login.TFrame", background=self.login_bg)

        welcome_label = ttk.Label(self.login_frame, 
                                text="Welcome to Inventory System", 
                                font=("Arial Black", 20),  # Slightly larger for login
                                foreground=self.welcome_color_main,
                                background=self.login_bg)
        welcome_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        ttk.Label(self.login_frame, text="Username:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.login_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        login_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        login_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        ttk.Label(self.login_frame, text="Default: Administrator", font=("Helvetica", 8)).grid(row=4, column=0, columnspan=2, pady=5)
        self.login_frame.grid_columnconfigure(1, weight=1)

    def login(self):  # Unchanged
        username = self.username_entry.get()
        password = self.password_entry.get()
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user or (username == DEFAULT_ADMIN_USERNAME and password == DEFAULT_ADMIN_PASSWORD):
            self.logged_in = True
            self.current_user = username
            self.login_frame.destroy()
            self.setup_main_interface()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        if not self.logged_in:
            messagebox.showerror("Error", "Please log in to register new users")
            return

        register_window = tk.Toplevel(self.root)
        register_window.title("Register New User")
        register_window.geometry("300x200")

        ttk.Label(register_window, text="New Username:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        new_username_entry = ttk.Entry(register_window)
        new_username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(register_window, text="New Password:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        new_password_entry = ttk.Entry(register_window, show="*")
        new_password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        def save_new_user():
            username = new_username_entry.get()
            password = new_password_entry.get()
            if not username or not password:
                messagebox.showerror("Error", "Username and password cannot be empty")
                return

            conn = sqlite3.connect(get_db_path())
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                messagebox.showinfo("Success", f"User '{username}' registered successfully")
                register_window.destroy()
                logging.info(f"User '{username}' registered by {self.current_user}")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists")
            conn.close()

        register_button = ttk.Button(register_window, text="Register", command=save_new_user)
        register_button.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        register_window.grid_columnconfigure(1, weight=1)

    def setup_main_interface(self):
        # Welcome Frame (reduced size)
        self.welcome_frame = tk.Frame(self.root, bg=self.welcome_bg)
        self.welcome_frame.pack(fill="x", pady=5)  # Keeping reduced pady
        self.welcome_frame.grid_columnconfigure(0, weight=1)

        welcome_text = "HarLuFran InnoFlux IMS - Inventory Management System"
        tagline_text = "Your Hub for Success"

        welcome_label = tk.Label(self.welcome_frame, 
                               text=welcome_text, 
                               font=("Montserrat", 20, "italic"),  
                               bg=self.welcome_bg, 
                               fg=self.welcome_color_main)
        welcome_label.pack(pady=1)

        tagline_label = tk.Label(self.welcome_frame, 
                               text=tagline_text, 
                               font=("Montserrat", 14, "bold"), 
                               bg=self.welcome_bg, 
                               fg=self.welcome_color_separator)
        tagline_label.pack(pady=1)

        # Notebook with colored tabs (unchanged)
        self.notebook = ttk.Notebook(self.root)
        self.store_tab = tk.Frame(self.notebook, bg=self.store_bg)
        self.lab_tab = tk.Frame(self.notebook, bg=self.lab_bg)
        self.analysis_tab = tk.Frame(self.notebook, bg=self.analysis_bg)
        self.history_tab = tk.Frame(self.notebook, bg=self.history_bg)
        self.settings_tab = tk.Frame(self.notebook, bg=self.settings_bg)
        
        self.notebook.add(self.store_tab, text="Store Inventory")
        self.notebook.add(self.lab_tab, text="Laboratory Inventory")
        self.notebook.add(self.analysis_tab, text="Analysis")
        self.notebook.add(self.history_tab, text="History")
        self.notebook.add(self.settings_tab, text="Settings")
        self.notebook.pack(expand=1, fill="both", padx=10, pady=5)

        # Rest of the method remains unchanged
        self.store_logic = StoreLogic(self, self.store_tab)
        self.lab_logic = LabLogic(self, self.lab_tab)

        self.setup_analysis_tab()
        self.setup_history_tab()
        self.setup_settings_tab()

        self.tooltip = None
        self.root.after(604800000, self.auto_backup)

        self.store_tab.grid_columnconfigure(0, weight=1)
        self.store_tab.grid_rowconfigure(0, weight=1)
        self.lab_tab.grid_columnconfigure(0, weight=1)
        self.lab_tab.grid_rowconfigure(0, weight=1)
        self.analysis_tab.grid_columnconfigure(0, weight=1)
        self.analysis_tab.grid_rowconfigure(0, weight=1)
        self.history_tab.grid_columnconfigure(0, weight=1)
        self.history_tab.grid_rowconfigure(0, weight=1)
        self.settings_tab.grid_columnconfigure(0, weight=1)
        self.settings_tab.grid_rowconfigure(0, weight=1)

    def setup_history_tab(self):
        # Create a canvas and scrollbar
        history_canvas = tk.Canvas(self.history_tab, bg=self.history_bg)
        scrollbar = ttk.Scrollbar(self.history_tab, orient="vertical", command=history_canvas.yview)
        
        # Create a frame inside the canvas
        history_frame = tk.Frame(history_canvas, bg=self.history_bg)
        
        # Configure the canvas
        history_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack the widgets
        scrollbar.pack(side="right", fill="y")
        history_canvas.pack(side="left", fill="both", expand=True)
        
        # Create window in canvas
        history_canvas.create_window((0, 0), window=history_frame, anchor="nw")
        
        # Create Treeview inside the frame
        self.history_tree = ttk.Treeview(history_frame, 
                                       columns=("ID", "Action", "Item ID", "Details", "Timestamp"), 
                                       show="headings")
        self.history_tree.heading("ID", text="ID")
        self.history_tree.heading("Action", text="Action")
        self.history_tree.heading("Item ID", text="Item ID")
        self.history_tree.heading("Details", text="Details")
        self.history_tree.heading("Timestamp", text="Timestamp")
        self.history_tree.pack(fill="both", expand=1, padx=10, pady=5)
        self.history_tree.configure(style="History.Treeview")
        self.style.configure("History.Treeview", background=self.history_bg)

        for col in ("ID", "Action", "Item ID", "Details", "Timestamp"):
            self.history_tree.column(col, stretch=tk.YES)
        
        # Update scroll region when frame size changes
        def configure_scroll(event):
            history_canvas.configure(scrollregion=history_canvas.bbox("all"))
        
        history_frame.bind("<Configure>", configure_scroll)
        
        self.load_history()


        
    def setup_analysis_tab(self):
        analysis_frame = ttk.LabelFrame(self.analysis_tab, text="Inventory Analysis")
        analysis_frame.pack(fill="both", expand=1, padx=10, pady=5)
        analysis_frame.configure(style="Analysis.TLabelframe")
        self.style.configure("Analysis.TLabelframe", background=self.analysis_bg)

        
        analysis_frame.columnconfigure(0, weight=1)
        analysis_frame.columnconfigure(1, weight=1)
        analysis_frame.rowconfigure(0, weight=1)
        analysis_frame.rowconfigure(1, weight=1)
        analysis_frame.rowconfigure(2, weight=1)
        analysis_frame.rowconfigure(3, weight=1)
        analysis_frame.rowconfigure(4, weight=1)

        ttk.Button(analysis_frame, text="Stock Summary (Store)", command=lambda: self.store_logic.show_stock_summary()).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        ttk.Button(analysis_frame, text="Stock Summary (Lab)", command=lambda: self.lab_logic.show_stock_summary()).grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        ttk.Button(analysis_frame, text="Low Stock Report (Store)", command=lambda: self.store_logic.low_stock_report()).grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        ttk.Button(analysis_frame, text="Low Stock Report (Lab)", command=lambda: self.lab_logic.low_stock_report()).grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        ttk.Button(analysis_frame, text="Category Analysis (Store)", command=lambda: self.store_logic.category_analysis()).grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        ttk.Button(analysis_frame, text="Category Analysis (Lab)", command=lambda: self.lab_logic.category_analysis()).grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        ttk.Button(analysis_frame, text="Issuance Trends (Store)", command=self.store_logic.issuance_trends).grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
        ttk.Button(analysis_frame, text="Broken Items Report (Lab)", command=self.lab_logic.broken_items_report).grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
        ttk.Button(analysis_frame, text="Predictive Reorder (Store)", command=lambda: self.store_logic.predictive_reorder()).grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
        ttk.Button(analysis_frame, text="Predictive Reorder (Lab)", command=lambda: self.lab_logic.predictive_reorder()).grid(row=4, column=1, padx=5, pady=5, sticky="nsew")

    

    

    def show_tooltip(self, event, text):
        if self.tooltip:
            self.hide_tooltip(event)
        self.tooltip = tk.Toplevel(self.root)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        label = tk.Label(self.tooltip, text=text, background="yellow", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

    def parse_quantity(self, qty_str):
        """Parse a quantity string into a number and unit (e.g., '10 mL' -> (10, 'mL'))."""
        if qty_str is None:
            return (0, '')
        qty_str = qty_str.strip()
        match = re.match(r"(\d+\.?\d*)\s*(\w+)", qty_str)
        if match:
            number, unit = match.groups()
            return (float(number), unit)
        return (0, '')

    def convert_units(self, qty, from_unit, to_unit):
        if from_unit in self.unit_conversions and to_unit in self.unit_conversions[from_unit]:
            return qty * self.unit_conversions[from_unit][to_unit]
        return qty


    def setup_settings_tab(self):
        settings_frame = ttk.LabelFrame(self.settings_tab, text="Settings")
        settings_frame.pack(fill="x", padx=10, pady=5)
        settings_frame.configure(style="Settings.TLabelframe")
        self.style.configure("Settings.TLabelframe", background=self.settings_bg)

        settings_frame.columnconfigure(0, weight=1)
        settings_frame.columnconfigure(1, weight=1)
        settings_frame.rowconfigure(0, weight=1)
        settings_frame.rowconfigure(1, weight=1)
        settings_frame.rowconfigure(2, weight=1)
        settings_frame.rowconfigure(3, weight=1)
        settings_frame.rowconfigure(4, weight=1)

        ttk.Label(settings_frame, text="Theme:").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.theme_var = tk.StringVar(value=self.theme)
        theme_combo = ttk.Combobox(settings_frame, textvariable=self.theme_var, values=["clam", "alt", "default"])
        theme_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.notify_var = tk.BooleanVar(value=self.notification_enabled)
        notify_check = ttk.Checkbutton(settings_frame, text="Enable Notifications", variable=self.notify_var, command=self.toggle_notifications)
        notify_check.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")

        backup_button = ttk.Button(settings_frame, text="Manual Backup", command=self.manual_backup)
        backup_button.grid(row=2, column=0, pady=10, sticky="ew")
        ttk.Label(settings_frame, text="Auto-backup every 7 days").grid(row=2, column=1, padx=5, pady=5, sticky="w")

        apply_button = ttk.Button(settings_frame, text="Apply Settings", command=self.apply_settings)
        apply_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        manage_users_button = ttk.Button(settings_frame, text="Manage Users", command=self.register)
        manage_users_button.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

    def load_history(self):
        self.history_tree.delete(*self.history_tree.get_children())
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        c.execute("SELECT id, action, item_id, details, timestamp FROM history")
        for row in c.fetchall():
            self.history_tree.insert("", "end", values=row)
        conn.close()

    def toggle_notifications(self):
        self.notification_enabled = self.notify_var.get()

    def apply_settings(self):
        new_theme = self.theme_var.get()
        if new_theme != self.theme:
            self.style.theme_use(new_theme)
            self.theme = new_theme
        messagebox.showinfo("Settings", "Settings applied successfully")

    def manual_backup(self):
        backup_dir = os.path.join(get_app_data_dir(), "backups")
        os.makedirs(backup_dir, exist_ok=True)
        backup_file = os.path.join(backup_dir, f"inventory_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
        shutil.copy2(get_db_path(), backup_file)
        messagebox.showinfo("Backup", f"Database backed up to {backup_file}")

    def auto_backup(self):
        self.manual_backup()
        self.root.after(604800000, self.auto_backup)

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()