# chemistry_practical.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import numpy as np
from collections import defaultdict
import re
import pyperclip
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Elements dictionary (molar masses)
elements = {
    "H": 1.01, "He": 4.00, "Li": 6.94, "Be": 9.01, "B": 10.81, "C": 12.01, "N": 14.01, "O": 16.00,
    "F": 19.00, "Ne": 20.18, "Na": 23.00, "Mg": 24.31, "Al": 26.98, "Si": 28.09, "P": 30.97, "S": 32.07,
    "Cl": 35.45, "Ar": 39.95, "K": 39.10, "Ca": 40.08, "Sc": 44.96, "Ti": 47.87, "V": 50.94, "Cr": 52.00,
    "Mn": 54.94, "Fe": 55.85, "Co": 58.93, "Ni": 58.69, "Cu": 63.55, "Zn": 65.38, "Ga": 69.72, "Ge": 72.63,
    "As": 74.92, "Se": 78.97, "Br": 79.90, "Kr": 83.80, "Rb": 85.47, "Sr": 87.62, "Y": 88.91, "Zr": 91.22,
    "Nb": 92.91, "Mo": 95.95, "Tc": 98.00, "Ru": 101.07, "Rh": 102.91, "Pd": 106.42, "Ag": 107.87, "Cd": 112.41,
    "In": 114.82, "Sn": 118.71, "Sb": 121.76, "Te": 127.60, "I": 126.90, "Xe": 131.29, "Cs": 132.91, "Ba": 137.33,
    "La": 138.91, "Ce": 140.12, "Pr": 140.91, "Nd": 144.24, "Pm": 145.00, "Sm": 150.36, "Eu": 151.96, "Gd": 157.25,
    "Tb": 158.93, "Dy": 162.50, "Ho": 164.93, "Er": 167.26, "Tm": 168.93, "Yb": 173.05, "Lu": 174.97, "Hf": 178.49,
    "Ta": 180.95, "W": 183.84, "Re": 186.21, "Os": 190.23, "Ir": 192.22, "Pt": 195.08, "Au": 196.97, "Hg": 200.59,
    "Tl": 204.38, "Pb": 207.20, "Bi": 208.98, "Po": 209.00, "At": 210.00, "Rn": 222.00, "Fr": 223.00, "Ra": 226.00,
    "Ac": 227.00, "Th": 232.04, "Pa": 231.04, "U": 238.03, "Np": 237.00, "Pu": 244.00, "Am": 243.00, "Cm": 247.00,
    "Bk": 247.00, "Cf": 251.00, "Es": 252.00, "Fm": 257.00, "Md": 258.00, "No": 259.00, "Lr": 262.00
}

# Expanded chemical data
chemical_data = {
    "Hydrochloric Acid (HCl)": {"stock_concentration": 12.0, "type": "liquid", "safety": "Corrosive. Wear gloves and goggles. Use in a well-ventilated area."},
    "Sodium Hydroxide (NaOH)": {"stock_concentration": None, "type": "solid", "safety": "Corrosive. Wear gloves and goggles. Avoid skin contact."},
    "Sulfuric Acid (H2SO4)": {"stock_concentration": 18.0, "type": "liquid", "safety": "Highly corrosive. Wear gloves and goggles. Add acid to water, not vice versa."},
    "Sodium Chloride (NaCl)": {"stock_concentration": None, "type": "solid", "safety": "Non-hazardous. Wear goggles as a precaution."},
    "Copper(II) Sulfate (CuSO4)": {"stock_concentration": None, "type": "solid", "safety": "Toxic if ingested. Wear gloves and goggles."},
    "Ethanol (C2H5OH)": {"stock_concentration": 95, "type": "liquid", "safety": "Flammable. Keep away from open flames. Use in a ventilated area."},
    "Sodium Bicarbonate (NaHCO3)": {"stock_concentration": None, "type": "solid", "safety": "Non-hazardous. Wear goggles as a precaution."},
    "Iron(III) Hydroxide (Fe(OH)3)": {"stock_concentration": None, "type": "solid", "safety": "May be irritating. Wear gloves and goggles."},
    "Potassium Permanganate (KMnO4)": {"stock_concentration": None, "type": "solid", "safety": "Oxidizer. Wear gloves and goggles. Avoid contact with combustibles."},
    "Calcium Carbonate (CaCO3)": {"stock_concentration": None, "type": "solid", "safety": "Non-hazardous. Wear goggles as a precaution."},
    "Magnesium Sulfate (MgSO4)": {"stock_concentration": None, "type": "solid", "safety": "Non-hazardous. Wear goggles as a precaution."},
    "Nitric Acid (HNO3)": {"stock_concentration": 15.0, "type": "liquid", "safety": "Corrosive and oxidizing. Wear gloves and goggles. Use in a fume hood."},
    "Ammonia (NH3)": {"stock_concentration": 15.0, "type": "liquid", "safety": "Corrosive and irritating. Wear gloves and goggles. Use in a well-ventilated area."},
    "Silver Nitrate (AgNO3)": {"stock_concentration": None, "type": "solid", "safety": "Toxic and corrosive. Wear gloves and goggles. Avoid skin contact."},
    "Zinc Chloride (ZnCl2)": {"stock_concentration": None, "type": "solid", "safety": "Corrosive. Wear gloves and goggles."},
    "Potassium Chloride (KCl)": {"stock_concentration": None, "type": "solid", "safety": "Non-hazardous. Wear goggles as a precaution."},
    "Sodium Sulfate (Na2SO4)": {"stock_concentration": None, "type": "solid", "safety": "Non-hazardous. Wear goggles as a precaution."},
    "Iron(II) Sulfate (FeSO4)": {"stock_concentration": None, "type": "solid", "safety": "Toxic if ingested. Wear gloves and goggles."},
    "Barium Chloride (BaCl2)": {"stock_concentration": None, "type": "solid", "safety": "Toxic. Wear gloves and goggles. Avoid ingestion."},
    "Lead(II) Nitrate (Pb(NO3)2)": {"stock_concentration": None, "type": "solid", "safety": "Toxic and hazardous. Wear gloves and goggles. Handle with care."},
    "Magnesium Chloride (MgCl2)": {"stock_concentration": None, "type": "solid", "safety": "Non-hazardous. Wear goggles as a precaution."},
    "Potassium Nitrate (KNO3)": {"stock_concentration": None, "type": "solid", "safety": "Oxidizer. Wear gloves and goggles. Avoid contact with combustibles."},
    "Calcium Chloride (CaCl2)": {"stock_concentration": None, "type": "solid", "safety": "Irritating. Wear gloves and goggles."},
    "Sodium Carbonate (Na2CO3)": {"stock_concentration": None, "type": "solid", "safety": "Irritating. Wear gloves and goggles."},
    "Copper(II) Nitrate (Cu(NO3)2)": {"stock_concentration": None, "type": "solid", "safety": "Toxic and corrosive. Wear gloves and goggles."},
    "Aluminum Sulfate (Al2(SO4)3)": {"stock_concentration": None, "type": "solid", "safety": "Irritating. Wear gloves and goggles."},
    "Phosphoric Acid (H3PO4)": {"stock_concentration": 14.6, "type": "liquid", "safety": "Corrosive. Wear gloves and goggles. Use in a well-ventilated area."},
    "Potassium Iodide (KI)": {"stock_concentration": None, "type": "solid", "safety": "May be irritating. Wear gloves and goggles."}
}

# Common volumetric flask sizes (mL)
flask_sizes = [10, 25, 50, 100, 250, 500, 1000, 2000]

def get_safety_info(formula):
    formula = formula.lower()
    if any(x in formula for x in ["hcl", "h2so4", "hno3", "h3po4"]):
        return "Corrosive. Wear gloves and goggles. Use in a well-ventilated area."
    elif "oh" in formula or "naoh" in formula:
        return "Corrosive. Wear gloves and goggles. Avoid skin contact."
    elif "c2h5oh" in formula:
        return "Flammable. Keep away from open flames. Use in a ventilated area."
    elif any(x in formula for x in ["cl", "br", "i"]):
        return "May be irritating or toxic. Wear gloves and goggles."
    elif "no3" in formula or "mno4" in formula:
        return "May be oxidizing or toxic. Wear gloves and goggles."
    return "Unknown safety info. Use caution."

def calculate_molar_mass(formula):
    formula = formula.replace(" ", "")
    if not re.match(r"^[A-Za-z0-9()]+$", formula):
        raise ValueError("Invalid formula: Use only letters, numbers, and parentheses.")
    total_mass = 0.0
    pattern = r"([A-Z][a-z]?)(\d*)|\((.*?)\)(\d*)"
    matches = re.finditer(pattern, formula)
    
    if not matches:
        raise ValueError("Invalid formula format.")
    
    for match in matches:
        if match.group(1):
            element = match.group(1)
            count = int(match.group(2)) if match.group(2) else 1
            if element in elements:
                total_mass += elements[element] * count
            else:
                raise ValueError(f"Unknown element: {element}")
        elif match.group(3):
            sub_formula = match.group(3)
            count = int(match.group(4)) if match.group(4) else 1
            sub_mass = calculate_molar_mass(sub_formula)
            total_mass += sub_mass * count
    
    return total_mass

def balance_equation(equation):
    equation = equation.replace("=", "->")
    if "->" not in equation:
        raise ValueError("Equation must contain '=' or '->' to separate reactants and products.")
    reactants, products = equation.split("->")
    reactants = [r.strip() for r in reactants.split("+")]
    products = [p.strip() for p in products.split("+")]

    def parse_formula_with_state(term):
        match = re.match(r"^(.*?)(?:\((s|l|g|aq)\))?$", term.strip())
        if not match:
            raise ValueError(f"Invalid term format: {term}")
        formula, state = match.groups(default="")
        elements_count = defaultdict(int)
        pattern = r"([A-Z][a-z]?)(\d*)|\((.*?)\)(\d*)"
        matches = re.finditer(pattern, formula)
        for match in matches:
            if match.group(1):
                element = match.group(1)
                count = int(match.group(2)) if match.group(2) else 1
                elements_count[element] += count
            elif match.group(3):
                sub_formula = match.group(3)
                count = int(match.group(4)) if match.group(4) else 1
                sub_counts = parse_formula_with_state(sub_formula)[0]
                for elem, num in sub_counts.items():
                    elements_count[elem] += num * count
        return elements_count, state

    reactant_elements = []
    reactant_states = []
    product_elements = []
    product_states = []
    for r in reactants:
        counts, state = parse_formula_with_state(r)
        reactant_elements.append(counts)
        reactant_states.append(state)
    for p in products:
        counts, state = parse_formula_with_state(p)
        product_elements.append(counts)
        product_states.append(state)

    all_elements = set()
    for r in reactant_elements:
        all_elements.update(r.keys())
    for p in product_elements:
        all_elements.update(p.keys())
    all_elements = list(all_elements)

    n_reactants = len(reactants)
    n_products = len(products)
    n_compounds = n_reactants + n_products
    matrix = np.zeros((len(all_elements), n_compounds))

    for i, elem in enumerate(all_elements):
        for j, counts in enumerate(reactant_elements):
            matrix[i, j] = counts.get(elem, 0)
        for j, counts in enumerate(product_elements):
            matrix[i, n_reactants + j] = -counts.get(elem, 0)

    try:
        augmented_matrix = np.vstack([matrix, [1] + [0] * (n_compounds - 1)])
        b = np.zeros(len(all_elements) + 1)
        b[-1] = 1
        coeffs = np.linalg.lstsq(augmented_matrix, b, rcond=None)[0]
        coeffs = coeffs / min(c for c in coeffs if c > 0.001)
        coeffs = np.round(coeffs).astype(int)

        balanced_r = [f"{c if c > 1 else ''}{r}{f'({s})' if s else ''}" for c, r, s in zip(coeffs[:n_reactants], reactants, reactant_states)]
        balanced_p = [f"{c if c > 1 else ''}{p}{f'({s})' if s else ''}" for c, p, s in zip(coeffs[n_reactants:], products, product_states)]
        return " + ".join(balanced_r) + " -> " + " + ".join(balanced_p)
    except np.linalg.LinAlgError:
        raise ValueError("Unable to balance equation (singular matrix or complex reaction).")

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event):
        if self.tip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT, background="#ffffe0", 
                         relief=tk.SOLID, borderwidth=1, font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

class SolutionCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(self.root)  
        
        # Configure grid weights for responsiveness
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=1)
        self.frame.rowconfigure(8, weight=1)

        # --- Row 0: Chemical Selection ---
        tk.Label(self.frame, text="Select Chemical or Enter Formula:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.chemical_var = tk.StringVar(value="Custom Formula")
        self.chemical_menu = ttk.Combobox(self.frame, textvariable=self.chemical_var, values=["Custom Formula"] + list(chemical_data.keys()))
        self.chemical_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ToolTip(self.chemical_menu, "Select a predefined chemical or choose 'Custom Formula' to enter your own.")
        self.formula_var = tk.StringVar()
        self.formula_entry = tk.Entry(self.frame, textvariable=self.formula_var)
        self.formula_entry.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        ToolTip(self.formula_entry, "Enter a chemical formula (e.g., H2O, NaCl) if using 'Custom Formula'.")
        tk.Button(self.frame, text="Verify Formula", command=self.verify_formula).grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # --- Row 1: Molar Mass ---
        tk.Label(self.frame, text="Molar Mass:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.molar_mass_var = tk.StringVar(value="N/A")
        tk.Label(self.frame, textvariable=self.molar_mass_var).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # --- Row 2: Concentration Type ---
        tk.Label(self.frame, text="Concentration Type:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.conc_type_var = tk.StringVar(value="Molarity (M)")
        self.conc_type_menu = ttk.Combobox(self.frame, textvariable=self.conc_type_var, values=["Molarity (M)", "Percentage (% w/v)", "Percentage (% v/v)"])
        self.conc_type_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ToolTip(self.conc_type_menu, "Choose the concentration type: Molarity (mol/L), % w/v (g/100 mL), or % v/v (mL/100 mL).")

        # --- Row 3: Concentration Value ---
        tk.Label(self.frame, text="Concentration Value:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.conc_value_var = tk.StringVar()
        self.conc_value_entry = tk.Entry(self.frame, textvariable=self.conc_value_var)
        self.conc_value_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        ToolTip(self.conc_value_entry, "Enter the desired concentration (e.g., 0.1 for 0.1 M, 5 for 5%).")

        # --- Row 4: Flask Sizes ---
        tk.Label(self.frame, text="Select Flask Sizes (mL):").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.flask_listbox = tk.Listbox(self.frame, selectmode="multiple", height=8, exportselection=0)
        for size in flask_sizes:
            self.flask_listbox.insert(tk.END, str(size))
        self.flask_listbox.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")
        self.flask_listbox.select_set(3)  # Default: 100 mL
        ToolTip(self.flask_listbox, "Select one or more flask sizes for the solution preparation.")
        tk.Button(self.frame, text="Select All", command=self.select_all_flasks).grid(row=4, column=2, padx=5, pady=5, sticky="ew")

        # --- Row 5: Stock Concentration ---
        tk.Label(self.frame, text="Stock Concentration (M or %):").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.stock_conc_var = tk.StringVar()
        self.stock_conc_entry = tk.Entry(self.frame, textvariable=self.stock_conc_var)
        self.stock_conc_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        ToolTip(self.stock_conc_entry, "Optional: Enter stock concentration if diluting (e.g., 12 for 12 M HCl).")

        button_frame_row6 = ttk.Frame(self.frame)
        button_frame_row6.grid(row=6, column=0, columnspan=4, padx=5, pady=5, sticky="ew")  # Fixed Rom4 to 4
        for i in range(6):
            button_frame_row6.columnconfigure(i, weight=1)

        ttk.Button(button_frame_row6, text="Calculate Solution", command=self.calculate_solution).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.show_safety_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(button_frame_row6, text="Show Safety Info", variable=self.show_safety_var).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ToolTip(button_frame_row6.winfo_children()[1], "Check to include safety precautions in the output.")
        ttk.Button(button_frame_row6, text="Save Output", command=self.save_output).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        ttk.Button(button_frame_row6, text="Clear Output", command=self.clear_output).grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        ttk.Button(button_frame_row6, text="Copy to Clipboard", command=self.copy_to_clipboard).grid(row=0, column=4, padx=5, pady=5, sticky="ew")
        ttk.Button(button_frame_row6, text="Bulk Preparation", command=self.open_bulk_window).grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        # --- Row 7: Equation Balancing ---
        equation_frame = ttk.Frame(self.frame)
        equation_frame.grid(row=7, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
        equation_frame.columnconfigure(1, weight=1)
        tk.Label(equation_frame, text="Enter Equation (e.g., MgCO3(s) + O2(g) = MgO(s) + CO2(g)):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.equation_var = tk.StringVar()
        self.equation_entry = tk.Entry(equation_frame, textvariable=self.equation_var, width=40)
        self.equation_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ToolTip(self.equation_entry, "Enter a chemical equation with states (s, l, g, aq), e.g., H2(g) + O2(g) = H2O(l).")
        ttk.Button(equation_frame, text="Balance Equation", command=self.balance_equation).grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # --- Row 8: Output Area ---
        output_frame = ttk.Frame(self.frame)
        output_frame.grid(row=8, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        output_frame.rowconfigure(0, weight=1)
        output_frame.columnconfigure(0, weight=1)

        self.output_tree = ttk.Treeview(output_frame, columns=("Flask Size", "Amount Needed", "Steps"), show="headings", height=5)
        self.output_tree.heading("Flask Size", text="Flask Size (mL)")
        self.output_tree.heading("Amount Needed", text="Amount Needed")
        self.output_tree.heading("Steps", text="Equipment & Steps")
        self.output_tree.column("Flask Size", width=100, anchor="center")
        self.output_tree.column("Amount Needed", width=150, anchor="center")
        self.output_tree.column("Steps", width=400, anchor="w", stretch=True)
        self.output_tree.grid(row=0, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.output_tree.configure(yscrollcommand=scrollbar.set)

        self.output_text = ScrolledText(output_frame, height=5, width=80)
        self.output_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.output_text.tag_configure("bold", font=("TkDefaultFont", 10, "bold"))

        # --- Row 9: Status Bar ---
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(self.frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor="w").grid(row=9, column=0, columnspan=4, sticky="ew", padx=5, pady=5)

        self.root.bind("<Configure>", self.on_resize)
    
    def on_resize(self, event):
        """Adjust Treeview column widths on resize."""
        if not hasattr(self, 'output_tree') or not self.output_tree.winfo_exists():
            return  # Skip if Treeview doesn’t exist
        try:
            width = self.root.winfo_width() - 40  # Account for padding and scrollbar
            self.output_tree.column("Flask Size", width=int(width * 0.15))
            self.output_tree.column("Amount Needed", width=int(width * 0.25))
            self.output_tree.column("Steps", width=int(width * 0.6), stretch=True)
        except tk.TclError:
            print("Treeview column adjustment skipped due to invalid state")# Dynamic width with stretch

    def adjust_treeview_height(self):
        num_rows = len(self.output_tree.get_children())
        new_height = max(5, min(num_rows + 2, 15))  # Min 5, max 15 rows
        self.output_tree.configure(height=new_height)

    def select_all_flasks(self):
        self.flask_listbox.select_set(0, tk.END)
        self.status_var.set("All flask sizes selected")

    def verify_formula(self):
        try:
            formula = self.formula_var.get().strip()
            if not formula and self.chemical_var.get() == "Custom Formula":
                raise ValueError("Please enter a formula.")
            elif self.chemical_var.get() != "Custom Formula":
                formula = self.chemical_var.get().split("(")[1].split(")")[0] if "(" in self.chemical_var.get() else self.chemical_var.get()
            
            molar_mass = calculate_molar_mass(formula)
            self.molar_mass_var.set(f"{molar_mass:.2f} g/mol")
            self.status_var.set(f"Formula verified: {molar_mass:.2f} g/mol")
            messagebox.showinfo("Success", f"Formula verified! Molar Mass: {molar_mass:.2f} g/mol")
        except ValueError as e:
            self.molar_mass_var.set("N/A")
            self.status_var.set("Error: Invalid formula")
            messagebox.showerror("Error", str(e))

    def calculate_solution(self):
        try:
            chemical = self.chemical_var.get()
            formula = self.formula_var.get().strip()
            conc_type = self.conc_type_var.get()
            conc_value = float(self.conc_value_var.get())
            selected_flasks = [int(self.flask_listbox.get(i)) for i in self.flask_listbox.curselection()]
            stock_conc = self.stock_conc_var.get().strip()

            if not selected_flasks:
                raise ValueError("Please select at least one flask size.")
            if conc_value <= 0:
                raise ValueError("Concentration value must be positive.")

            if chemical == "Custom Formula" and not formula:
                raise ValueError("Please enter a chemical formula.")
            elif chemical != "Custom Formula":
                formula = chemical.split("(")[1].split(")")[0] if "(" in chemical else chemical
                chem_info = chemical_data.get(chemical, {"type": "solid", "stock_concentration": None, "safety": "Unknown safety info. Use caution."})
            else:
                chem_info = {"type": "solid", "stock_concentration": None, "safety": get_safety_info(formula)}

            if stock_conc:
                try:
                    stock_conc_value = float(stock_conc)
                    if stock_conc_value <= 0:
                        raise ValueError("Stock concentration must be positive.")
                    chem_info["stock_concentration"] = stock_conc_value
                    chem_info["type"] = "liquid" if conc_type in ["Molarity (M)", "Percentage (% v/v)"] else chem_info["type"]
                except ValueError as e:
                    raise ValueError(f"Invalid stock concentration: {str(e)}")

            molar_mass = calculate_molar_mass(formula)
            display_name = chemical if chemical != "Custom Formula" else formula

            for item in self.output_tree.get_children():
                self.output_tree.delete(item)
            self.output_text.delete(1.0, tk.END)

            self.output_text.insert(tk.END, f"Solution Preparation Report for {conc_value} {conc_type} {display_name}\n", "bold")
            self.output_text.insert(tk.END, f"Molar Mass: {molar_mass:.2f} g/mol\n\n")

            for flask_size in selected_flasks:
                volume = flask_size / 1000
                if conc_type == "Molarity (M)":
                    moles = conc_value * volume
                    if chem_info["type"] == "solid" or chem_info["stock_concentration"] is None:
                        grams = moles * molar_mass
                        precision = "0.1 mg" if grams < 0.1 else "1 mg" if grams < 1 else "10 mg"
                        balance = "Ohaus Navigator" if grams < 1 else "Sartorius Entris"
                        amount = f"{grams:.4f} g"
                        steps = (
                            f"1. Weigh {grams:.4f} g using {balance} (precision: {precision})\n"
                            f"2. Transfer to {flask_size//2} mL beaker with distilled water\n"
                            f"3. Stir with magnetic stirrer until dissolved\n"
                            f"4. Transfer to {flask_size} mL flask via funnel\n"
                            f"5. Rinse beaker/funnel, add to flask\n"
                            f"6. Fill to mark with water, mix"
                        )
                    else:
                        stock_molarity = chem_info["stock_concentration"]
                        stock_volume = (moles / stock_molarity) * 1000
                        if stock_volume > 15:
                            pipet = "Fixed 25 mL Pipette"
                        elif stock_volume > 5:
                            pipet = "Fixed 10 mL Pipette"
                        else:
                            pipet = "Gilson Pipetman (5 mL)"
                        amount = f"{stock_volume:.4f} mL"
                        steps = (
                            f"1. Measure {stock_volume:.4f} mL with {pipet}\n"
                            f"2. Transfer to {flask_size} mL flask\n"
                            f"3. Fill to mark with water, mix"
                        )

                elif conc_type == "Percentage (% w/v)":
                    grams = (conc_value / 100) * flask_size
                    precision = "0.1 mg" if grams < 0.1 else "1 mg" if grams < 1 else "10 mg"
                    balance = "Ohaus Navigator" if grams < 1 else "Sartorius Entris"
                    amount = f"{grams:.4f} g"
                    steps = (
                        f"1. Weigh {grams:.4f} g using {balance} (precision: {precision})\n"
                        f"2. Transfer to {flask_size//2} mL beaker with distilled water\n"
                        f"3. Stir with magnetic stirrer until dissolved\n"
                        f"4. Transfer to {flask_size} mL flask via funnel\n"
                        f"5. Rinse beaker/funnel, add to flask\n"
                        f"6. Fill to mark with water, mix"
                    )

                elif conc_type == "Percentage (% v/v)":
                    if chem_info["type"] == "liquid" and chem_info["stock_concentration"]:
                        stock_percent = chem_info["stock_concentration"]
                        stock_volume = (conc_value / stock_percent) * flask_size
                        if stock_volume > 15:
                            pipet = "Fixed 25 mL Pipette"
                        elif stock_volume > 5:
                            pipet = "Fixed 10 mL Pipette"
                        else:
                            pipet = "Gilson Pipetman (5 mL)"
                        amount = f"{stock_volume:.4f} mL"
                        steps = (
                            f"1. Measure {stock_volume:.4f} mL with {pipet}\n"
                            f"2. Transfer to {flask_size} mL flask\n"
                            f"3. Fill to mark with water, mix"
                        )
                    else:
                        raise ValueError("Percentage (% v/v) requires a liquid with a stock concentration.")

                self.output_tree.insert("", "end", values=(flask_size, amount, steps))

            self.adjust_treeview_height()  # Adjust height after inserting rows

            if self.show_safety_var.get():
                self.output_text.insert(tk.END, "\nSafety Precautions (Applicable to All Sizes):\n", "bold")
                self.output_text.insert(tk.END, chem_info["safety"] + "\n")
                self.output_text.insert(tk.END, "General: Wear PPE (goggles, gloves). Ensure ventilation. Label the solution.")
            self.status_var.set(f"Report generated for {display_name}")

        except ValueError as e:
            self.status_var.set("Error: Invalid input")
            messagebox.showerror("Error", str(e))
        except Exception as e:
            self.status_var.set("Error: Calculation failed")
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def balance_equation(self):
        try:
            equation = self.equation_var.get().strip()
            if not equation:
                raise ValueError("Please enter a chemical equation.")
            balanced = balance_equation(equation)
            for item in self.output_tree.get_children():
                self.output_tree.delete(item)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Balanced Equation:\n", "bold")
            self.output_text.insert(tk.END, balanced + "\n")
            self.status_var.set("Equation balanced")
        except ValueError as e:
            self.status_var.set("Error: Invalid equation")
            messagebox.showerror("Error", str(e))
        except Exception as e:
            self.status_var.set("Error: Balancing failed")
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def open_bulk_window(self):
        bulk_window = tk.Toplevel(self.root)
        bulk_window.title("Bulk Preparation Calculator")
        bulk_window.geometry("600x500")
        bulk_window.columnconfigure(1, weight=1)
        bulk_window.rowconfigure(5, weight=1)

        # Number of students
        tk.Label(bulk_window, text="Number of Students:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.num_students_var = tk.StringVar(value="200")
        tk.Entry(bulk_window, textvariable=self.num_students_var).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ToolTip(bulk_window.winfo_children()[-1], "Enter the number of students (e.g., 200).")

        # Volume per student
        tk.Label(bulk_window, text="Volume per Student (mL):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.volume_per_student_var = tk.StringVar(value="10")
        volume_options = ["5", "10", "15", "20", "Custom"]
        self.volume_menu = ttk.Combobox(bulk_window, textvariable=self.volume_per_student_var, values=volume_options)
        self.volume_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.volume_menu.bind("<<ComboboxSelected>>", self.on_volume_select)
        ToolTip(self.volume_menu, "Select a common volume or 'Custom' to enter your own.")
        self.custom_volume_entry = tk.Entry(bulk_window, textvariable=self.volume_per_student_var, state="disabled")
        self.custom_volume_entry.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        # Extra volume percentage
        tk.Label(bulk_window, text="Extra Volume (%):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.extra_volume_var = tk.StringVar(value="10")
        tk.Entry(bulk_window, textvariable=self.extra_volume_var).grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ToolTip(bulk_window.winfo_children()[-1], "Enter extra volume percentage for waste/spares (e.g., 10 for 10%).")

        # Preferred flask sizes
        tk.Label(bulk_window, text="Preferred Flask Sizes (mL):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.bulk_flask_listbox = tk.Listbox(bulk_window, selectmode="multiple", height=5, exportselection=0)
        for size in flask_sizes:
            self.bulk_flask_listbox.insert(tk.END, str(size))
        self.bulk_flask_listbox.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
        self.bulk_flask_listbox.select_set(0, tk.END)  # Default: all selected
        ToolTip(self.bulk_flask_listbox, "Select preferred flask sizes for bulk preparation.")

        # Buttons
        button_frame = ttk.Frame(bulk_window)
        button_frame.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        ttk.Button(button_frame, text="Calculate Bulk Preparation", command=self.calculate_bulk).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Save as PDF", command=self.save_bulk_pdf).grid(row=0, column=1, padx=5, pady=5)

        # Output text
        self.bulk_output_text = ScrolledText(bulk_window, height=15, width=70)
        self.bulk_output_text.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        self.bulk_output_text.tag_configure("bold", font=("TkDefaultFont", 10, "bold"))
    
    def on_volume_select(self, event):
        if self.volume_menu.get() == "Custom":
            self.custom_volume_entry.config(state="normal")
            self.custom_volume_entry.focus_set()
        else:
            self.custom_volume_entry.config(state="disabled")
            self.volume_per_student_var.set(self.volume_menu.get())

    def calculate_bulk(self):
        try:
            chemical = self.chemical_var.get()
            formula = self.formula_var.get().strip()
            conc_type = self.conc_type_var.get()
            conc_value = float(self.conc_value_var.get())
            stock_conc = self.stock_conc_var.get().strip()
            num_students = int(self.num_students_var.get())
            volume_per_student = float(self.volume_per_student_var.get())
            extra_volume_percent = float(self.extra_volume_var.get())

            if num_students <= 0 or volume_per_student <= 0 or extra_volume_percent < 0:
                raise ValueError("Number of students, volume per student, and extra volume must be non-negative.")
            if chemical == "Custom Formula" and not formula:
                raise ValueError("Please enter a chemical formula.")
            elif chemical != "Custom Formula":
                formula = chemical.split("(")[1].split(")")[0] if "(" in chemical else chemical
                chem_info = chemical_data.get(chemical, {"type": "solid", "stock_concentration": None, "safety": "Unknown safety info. Use caution."})
            else:
                chem_info = {"type": "solid", "stock_concentration": None, "safety": get_safety_info(formula)}

            if stock_conc:
                stock_conc_value = float(stock_conc)
                if stock_conc_value <= 0:
                    raise ValueError("Stock concentration must be positive.")
                chem_info["stock_concentration"] = stock_conc_value
                chem_info["type"] = "liquid" if conc_type in ["Molarity (M)", "Percentage (% v/v)"] else chem_info["type"]

            molar_mass = calculate_molar_mass(formula)
            display_name = chemical if chemical != "Custom Formula" else formula

            base_volume = num_students * volume_per_student / 1000  # Convert to liters
            extra_volume = base_volume * (extra_volume_percent / 100)
            total_volume = base_volume + extra_volume

            self.bulk_output_text.delete(1.0, tk.END)
            self.bulk_output_text.insert(tk.END, f"Bulk Preparation for {num_students} Students\n", "bold")
            self.bulk_output_text.insert(tk.END, f"Concentration: {conc_value} {conc_type} {display_name}\n")
            self.bulk_output_text.insert(tk.END, f"Volume per Student: {volume_per_student} mL\n")
            self.bulk_output_text.insert(tk.END, f"Base Volume Required: {base_volume * 1000:.2f} mL ({base_volume:.2f} L)\n")
            self.bulk_output_text.insert(tk.END, f"Extra Volume ({extra_volume_percent}%): {extra_volume * 1000:.2f} mL ({extra_volume:.2f} L)\n")
            self.bulk_output_text.insert(tk.END, f"Total Volume Required: {total_volume * 1000:.2f} mL ({total_volume:.2f} L)\n\n")

            if conc_type == "Molarity (M)":
                total_moles = conc_value * total_volume
                if chem_info["type"] == "solid" or chem_info["stock_concentration"] is None:
                    total_grams = total_moles * molar_mass
                    self.bulk_output_text.insert(tk.END, f"Total Amount Needed: {total_grams:.2f} g of {display_name}\n")
                else:
                    stock_molarity = chem_info["stock_concentration"]
                    total_stock_volume = (total_moles / stock_molarity) * 1000
                    self.bulk_output_text.insert(tk.END, f"Total Stock Solution Needed: {total_stock_volume:.2f} mL of {stock_molarity} M {display_name}\n")

            elif conc_type == "Percentage (% w/v)":
                total_grams = (conc_value / 100) * (total_volume * 1000)
                self.bulk_output_text.insert(tk.END, f"Total Amount Needed: {total_grams:.2f} g of {display_name}\n")

            elif conc_type == "Percentage (% v/v)":
                if chem_info["type"] == "liquid" and chem_info["stock_concentration"]:
                    stock_percent = chem_info["stock_concentration"]
                    total_stock_volume = (conc_value / stock_percent) * (total_volume * 1000)
                    self.bulk_output_text.insert(tk.END, f"Total Stock Solution Needed: {total_stock_volume:.2f} mL of {stock_percent}% {display_name}\n")
                else:
                    raise ValueError("Percentage (% v/v) requires a liquid with a stock concentration.")

            self.bulk_output_text.insert(tk.END, "\nSuggested Batch Preparation:\n", "bold")
            preferred_flasks = [int(self.bulk_flask_listbox.get(i)) for i in self.bulk_flask_listbox.curselection()]
            if not preferred_flasks:
                preferred_flasks = flask_sizes  # Fallback to all sizes if none selected
            remaining_volume = total_volume * 1000
            for flask_size in sorted(preferred_flasks, reverse=True):
                num_batches = int(remaining_volume // flask_size)
                if num_batches > 0:
                    self.bulk_output_text.insert(tk.END, f"- Prepare {num_batches} x {flask_size} mL flasks\n")
                    remaining_volume -= num_batches * flask_size
            if remaining_volume > 0:
                self.bulk_output_text.insert(tk.END, f"- Prepare 1 x {min(preferred_flasks, key=lambda x: abs(x - remaining_volume))} mL flask for remaining {remaining_volume:.2f} mL\n")

            self.status_var.set(f"Bulk preparation calculated for {num_students} students")

        except ValueError as e:
            self.status_var.set("Error: Invalid input in bulk preparation")
            messagebox.showerror("Error", str(e))
        except Exception as e:
            self.status_var.set("Error: Bulk calculation failed")
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def save_bulk_pdf(self):
        output = self.bulk_output_text.get(1.0, tk.END).strip()
        if not output:
            self.status_var.set("Warning: No bulk output to save")
            messagebox.showwarning("Warning", "No bulk output to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
        if file_path:
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            for line in output.split("\n"):
                if line.endswith(":"):
                    story.append(Paragraph(line, styles["Heading2"]))
                else:
                    story.append(Paragraph(line, styles["BodyText"]))
                story.append(Spacer(1, 12))
            
            doc.build(story)
            self.status_var.set(f"Bulk output saved as PDF to {file_path}")
            messagebox.showinfo("Success", f"Bulk output saved as PDF to {file_path}")

    def save_output(self):
        output = self._get_full_output()
        if not output:
            self.status_var.set("Warning: No output to save")
            messagebox.showwarning("Warning", "No output to save.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(output)
            self.status_var.set(f"Output saved to {file_path}")
            messagebox.showinfo("Success", f"Output saved to {file_path}")

    def clear_output(self):
        for item in self.output_tree.get_children():
            self.output_tree.delete(item)
        self.output_text.delete(1.0, tk.END)
        self.output_tree.configure(height=5)  # Reset height
        self.status_var.set("Output cleared")

    def copy_to_clipboard(self):
        output = self._get_full_output()
        if not output:
            self.status_var.set("Warning: No output to copy")
            messagebox.showwarning("Warning", "No output to copy.")
            return
        pyperclip.copy(output)
        self.status_var.set("Output copied to clipboard")
        messagebox.showinfo("Success", "Output copied to clipboard")

    def _get_full_output(self):
        output = self.output_text.get(1.0, tk.END).strip()
        if self.output_tree.get_children():
            output += "\n\nPreparation Details:\n"
            output += "Flask Size (mL) | Amount Needed | Equipment & Steps\n"
            output += "-" * 80 + "\n"
            for item in self.output_tree.get_children():
                flask_size, amount, steps = self.output_tree.item(item, "values")
                output += f"{flask_size:<15} | {amount:<15} | {steps}\n"
        return output.strip()

if __name__ == "__main__":
    root = tk.Tk()
    app = SolutionCalculatorApp(root)
    root.mainloop()