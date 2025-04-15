

# HarLuFran InnoFlux IMS - Inventory Management System

![License](https://img.shields.io/badge/license-MIT-blue.svg)
**Version**: 1.0  
**Last Updated**: April 14, 2025  

The HarLuFran InnoFlux Inventory Management System (IMS) is a Python-based desktop application for managing inventory in educational institutions, focusing on store and laboratory environments. Built with Tkinter for the GUI and SQLite for data storage, it supports item tracking, lab practical planning, chemical preparation, and reporting. Key features include chemical equation balancing, solution preparation, and predictive reordering.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
  - [Functions of the Files](#functions-of-the-files)
- [License](#license)
- [Contact](#contact)

## Features
- Secure user authentication and registration.
- Multi-tab GUI for Store, Lab, Analysis, History, and Settings.
- Manage items, track batches, and report broken equipment.
- Plan chemistry practicals with solution calculations and equation balancing.
- Generate stock reports, trends, and predictive reordering.
- Customize themes, notifications, and backups.
- 
## Usage

Login
- Use default credentials: Username: admin, Password: harry20070465.
- Register new users via the Settings tab after logging in.
  
Store Inventory

- Navigate to the Store Inventory tab.
- Add Items: Enter details like name, category, quantity, reorder level, and expiry date.
- Issue Items: Record issuances to track usage.
- Generate Reports: Create stock summaries, low stock alerts, or category analyses, and export as CSV, Excel, or PDF.
- Batch Tracking: Manage item batches with batch numbers and costs.
  
Laboratory Inventory

- Go to the Laboratory Inventory tab.
- Manage Items: Add/edit lab items by subject (e.g., Chemistry, Physics), including molarity and purchase units.
- Plan Practicals: Schedule practicals, specify student numbers, groups, and chemicals, and verify material availability.
- Report Broken Items: Log damaged equipment with student details and track status (Pending/Resolved).
- GMP Analysis: Run compliance checks for lab processes.
- Reports: Generate practical reports or broken item logs, exportable as CSV, Excel, or PDF.
  
Chemistry Practical Planning

- In the Laboratory Inventory tab, select Plan Chemistry Practical.
- Select Chemical: Choose from predefined chemicals or enter a custom formula (e.g., H2SO4).
- Specify Concentration: Enter molarity (M), % w/v, or % v/v, and select flask sizes (e.g., 100 mL, 250 mL).
- Calculate: Generate preparation steps (e.g., weigh 5.4321 g, dissolve in flask).
- Balance Equations: Input equations (e.g., H2 + O2 = H2O) to balance with states (s, l, g, aq).
- Bulk Preparation: Plan for large classes, specifying students, volume per student, and extra volume percentage.
- Output: Save results as text or PDF, copy to clipboard, or clear.
  
Analysis

- Access the Analysis tab for reports:
- Stock Summaries: Overview of store and lab inventory.
- Low Stock Alerts: Identify items below reorder levels.
- Category Analyses: Breakdown by item categories.
- Issuance Trends: Track usage over time.
- Broken Items: Lab-specific damage reports.
- Predictive Reordering: Forecast restocking needs.
  
History

- View the History tab for an audit trail of actions (e.g., item added, issued, deleted) with timestamps and item IDs.
  
Settings

- In the Settings tab:
- Change Theme: Select clam, alt, or default.
- Toggle Notifications: Enable/disable alerts for low stock or expiries.
- Manage Users: Register new users with unique credentials.
- Backup: Perform manual database backups (auto-backups occur every 7 days).

## Directory Structure

harlufran-innoflux-ims/
- ├── inventory.py              # Main application entry point
- ├── store_logic.py            # Store inventory logic
- ├── lab_logic.py              # Laboratory inventory logic
- ├── chemistry_practical.py    # Chemistry practical planning
- ├── requirements.txt          # Python dependencies
- ├── LICENSE                   # MIT License
- ├── .gitignore                # Git exclusions
- ├── schema.sql                # Database schema
- ├── CONTRIBUTING.md           # Contribution guidelines
- ├── inventory.db              # SQLite database (generated on first run)
- ├── backups/                  # Database backups
- └── logs/                     # Application logs

## Functions of the Files

inventory.py

  Purpose: Serves as the main entry point for the application, initializing the GUI and database.

  Key Functions:

- Initializes the SQLite database (inventory.db) with tables for items, users, history, etc.
- Sets up the Tkinter interface with tabs for Store, Lab, Analysis, History, and Settings.
- Handles user authentication (login, registration) and session management.
- Manages backups (manual and auto every 7 days) and logging to inventory_app.log.
- Coordinates interactions between store and lab modules via StoreLogic and LabLogic classes.
  
store_logic.py

  Purpose: Manages store inventory operations and reporting.

  Key Functions:

- Adds, edits, deletes, and issues items with details like quantity, category, and expiry date.
- Tracks item batches with batch numbers, costs, and dates.
- Generates reports: stock summaries, low stock alerts, category analyses, and issuance trends.
- Supports predictive reordering based on usage patterns.
- Exports reports as CSV, Excel, or PDF using openpyxl and reportlab.
  
lab_logic.py

  Purpose: Handles laboratory inventory and practical planning.
  
  Key Functions:

- Manages lab items by subject (e.g., Chemistry, Physics) with molarity and unit details.
- Plans and schedules lab practicals, verifying material availability for students.
- Logs and tracks broken items with student details and status.
- Performs GMP (Good Manufacturing Practices) analysis for compliance.
- Integrates with chemistry_practical.py for chemical planning.
- Generates reports (practicals, broken items, predictive reordering) exportable as CSV, Excel, or PDF.
  
chemistry_practical.py
  
  Purpose: Provides tools for chemistry practical planning and calculations.
  
  Key Functions:

- Calculates solution preparations (molarity, % w/v, % v/v) for specified flask sizes, with detailed steps.
- Computes molar masses for custom or predefined chemicals using a periodic table dictionary.
- Balances chemical equations using linear algebra (numpy), supporting states (s, l, g, aq).
- Plans bulk preparations for large classes, accounting for extra volume.
- Displays safety precautions for chemicals.
- Outputs results as text, PDF (reportlab), or clipboard (pyperclip).
  
requirements.txt

  Purpose: Lists Python dependencies required to run the application.
  
  Key Functions:
  
- Specifies libraries: numpy, reportlab, openpyxl, matplotlib, scipy, statsmodels, constraint, plyer, pyperclip.
- Enables easy installation with pip install -r requirements.txt.
  
LICENSE

  Purpose: Defines the MIT License terms for using and distributing the software.
  
  Key Functions:

- Grants permission to use, modify, and share the code, retaining the copyright notice.
- Disclaims warranties and liabilities.
  
.gitignore

  Purpose: Excludes unnecessary or sensitive files from Git version control.
  
  Key Functions:

- Ignores generated files (inventory.db, backups/, logs/), Python bytecode (__pycache__, *.pyc), and build artifacts (dist/, *.exe).
- Prevents committing IDE configs (.vscode/, .idea/) and virtual environments (venv/).
  
schema.sql

   Purpose: Defines the database schema for manual initialization.
  
  Key Functions:

- Creates tables for items, users, history, etc.
- Includes default admin user.
  
CONTRIBUTING.md

   Purpose: Guides contributors on how to contribute.
   
   Key Functions:

- Outlines forking, branching, and PR processes.
- Specifies coding and testing guidelines.

Database Schema

- items: id (PK), name, category, quantity, reorder_level, section, subject, last_updated, expiry_date, purchase_unit, molarity, calories, protein
- issuance: id (PK), item_id (FK), person_name, quantity_issued, issue_date
- broken_items: id (PK), student_id, student_name, item_id (FK), item_name, report_date, status
- history: id (PK), action, item_id (FK), details, timestamp
- users: id (PK), username, password
- practical_reports: id (PK), subject, form, num_students, topic, subtopic, time, status
- prices: item_id (FK), price, last_updated
- invoices: id (PK), supplier, item_id (FK), quantity, price, invoice_date
- meal_templates: id (PK), name, requirements
- batches: id (PK), item_id (FK), batch_number, quantity, unit_cost, received_date, expiry_date
  
## License
This project is licensed under the MIT License. See the  file for details.

## Contact

- Maintainer: Harry Oginga
- Email: harryoginga@gmail.com
- GitHub: harry647/harlufran-innoflux-ims

## Installation
- Install Dependencies
- Initialize the Database
- Run inventory.py to create inventory.db in:
. Windows: C:\Users\<User>\AppData\Roaming\InventoryManagementSystem
. macOS/Linux: ~/.InventoryManagementSystem
  
- Optional: Build Executable
- Create a standalone executable with PyInstaller:
- Ensure inventory.db is included for first-time use.
  
### Clone the Repository
```bash
git clone https://github.com/harry647/harlufran-innoflux-ims.git
cd harlufran-innoflux-ims

[![CI](https://github.com/harry647/harlufran-innoflux-ims/actions/workflows/ci.yml/badge.svg)](https://github.com/harry647/harlufran-innoflux-ims/actions/workflows/ci.yml)

pip install -r requirements.txt

python inventory.py

pyinstaller --onefile --add-data "inventory.db;." inventory.py

