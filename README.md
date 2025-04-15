

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

## Installation
### Clone the Repository
```bash
git clone https://github.com/harry647/harlufran-innoflux-ims.git
cd harlufran-innoflux-ims

[![CI](https://github.com/harry647/harlufran-innoflux-ims/actions/workflows/ci.yml/badge.svg)](https://github.com/harry647/harlufran-innoflux-ims/actions/workflows/ci.yml)

