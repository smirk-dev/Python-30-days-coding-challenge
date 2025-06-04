import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import pandas as pd
# Constants for styling
BG_COLOR = "#121212"  # Dark background
CARD_COLOR = "#1E1E1E"  # Slightly lighter background for "cards"
TEXT_COLOR = "#FFFFFF"  # White text
ACCENT_COLOR = "#A385FF"  # Light purple for accents
# Database and budget settings
DB_NAME = "expenses.db"
BUDGET = 1000  # Example monthly budget
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     amount REAL NOT NULL,
                     category TEXT NOT NULL,
                     description TEXT,
                     payment_method TEXT,
                     date TEXT NOT NULL)''')
        conn.commit()
class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("1000x800")
        self.root.configure(bg=BG_COLOR)
        # Initialize database
        init_db()
        # Main frames
        self.input_frame = tk.Frame(root, bg=BG_COLOR, padx=10, pady=10)
        self.input_frame.pack(pady=10, fill=tk.X)
        self.filter_frame = tk.Frame(root, bg=BG_COLOR, padx=10, pady=10)
        self.filter_frame.pack(pady=5, fill=tk.X)
        self.table_frame = tk.Frame(root, bg=BG_COLOR)
        self.table_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        self.graph_frame = tk.Frame(root, bg=BG_COLOR)
        self.graph_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        # Title
        title = tk.Label(root, text="Expense Tracker", fg=TEXT_COLOR, bg=BG_COLOR, font=("Arial", 18, "bold"))
        title.pack(pady=10)
        # Input widgets
        self.create_input_widgets()
        # Filter widgets
        self.create_filter_widgets()
        # Expense table
        self.tree = ttk.Treeview(self.table_frame, columns=("Amount", "Category", "Payment Method", "Description", "Date"), show="headings", style="Custom.Treeview")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Payment Method", text="Payment Method")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Date", text="Date")
        self.tree.pack(fill=tk.BOTH, expand=True)
        # Configure Treeview style
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Custom.Treeview", 
                        background=CARD_COLOR, 
                        fieldbackground=CARD_COLOR, 
                        foreground=TEXT_COLOR)
        style.map('Custom.Treeview', 
                  background=[('selected', ACCENT_COLOR)])
        # Load data
        self.load_expenses()
    def create_input_widgets(self):
        # Amount
        tk.Label(self.input_frame, text="Amount:", fg=TEXT_COLOR, bg=BG_COLOR).grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(self.input_frame)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)
        # Category
        tk.Label(self.input_frame, text="Category:", fg=TEXT_COLOR, bg=BG_COLOR).grid(row=0, column=2, padx=5, pady=5)
        self.category_entry = ttk.Combobox(self.input_frame, values=["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"], style="Custom.TCombobox")
        self.category_entry.grid(row=0, column=3, padx=5, pady=5)
        # Payment Method
        tk.Label(self.input_frame, text="Payment Method:", fg=TEXT_COLOR, bg=BG_COLOR).grid(row=0, column=4, padx=5, pady=5)
        self.payment_entry = ttk.Combobox(self.input_frame, values=["Cash", "Credit Card", "UPI", "Other"], style="Custom.TCombobox")
        self.payment_entry.grid(row=0, column=5, padx=5, pady=5)
        # Description
        tk.Label(self.input_frame, text="Description:", fg=TEXT_COLOR, bg=BG_COLOR).grid(row=0, column=6, padx=5, pady=5)
        self.desc_entry = ttk.Entry(self.input_frame, width=30)
        self.desc_entry.grid(row=0, column=7, padx=5, pady=5)
        # Date
        tk.Label(self.input_frame, text="Date:", fg=TEXT_COLOR, bg=BG_COLOR).grid(row=1, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(self.input_frame)
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        # Buttons
        tk.Button(self.input_frame, text="Add Expense", command=self.add_expense, bg=ACCENT_COLOR, fg="black").grid(row=1, column=2, padx=5, pady=5)
        tk.Button(self.input_frame, text="Export to CSV", command=self.export_to_csv, bg=ACCENT_COLOR, fg="black").grid(row=1, column=3, padx=5, pady=5)
        tk.Button(self.input_frame, text="Generate Graph", command=self.generate_graph, bg=ACCENT_COLOR, fg="black").grid(row=1, column=4, padx=5, pady=5)
    def create_filter_widgets(self):
        tk.Label(self.filter_frame, text="Filter By:", fg=TEXT_COLOR, bg=BG_COLOR).grid(row=0, column=0, padx=5, pady=5)
        self.filter_combobox = ttk.Combobox(self.filter_frame, values=["All", "Weekly", "Monthly", "Yearly"], state="readonly", style="Custom.TCombobox")
        self.filter_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.filter_combobox.current(0)
        tk.Button(self.filter_frame, text="Apply Filter", command=self.load_expenses, bg=ACCENT_COLOR, fg="black").grid(row=0, column=2, padx=5, pady=5)
        # Configure Combobox style
        style = ttk.Style()
        style.configure("Custom.TCombobox", 
                        background=CARD_COLOR, 
                        foreground=TEXT_COLOR)
    def add_expense(self):
        """Add an expense to the database."""
        try:
            # Get input values
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            payment = self.payment_entry.get()
            description = self.desc_entry.get()
            date = self.date_entry.get()
            # Validate required fields
            if not category or not payment or not amount:
                messagebox.showerror("Error", "Please fill in all fields")
                return
            # Validate date format
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
                return
            # Insert into the database
            with sqlite3.connect(DB_NAME) as conn:
                c = conn.cursor()
                c.execute("INSERT INTO expenses (amount, category, payment_method, description, date) VALUES (?, ?, ?, ?, ?)",
                          (amount, category, payment, description, date))
                conn.commit()
            messagebox.showinfo("Success", "Expense added successfully!")
            self.check_budget_alert()
            self.load_expenses()
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
    def load_expenses(self):
        filter_option = self.filter_combobox.get()
        for row in self.tree.get_children():
            self.tree.delete(row)
        query = "SELECT amount, category, payment_method, description, date FROM expenses"
        params = []
        current_time = datetime.now()
        if filter_option == "Weekly":
            last_week = current_time - timedelta(weeks=1)
            query += " WHERE date >= ?"
            params.append(last_week.strftime("%Y-%m-%d"))
        elif filter_option == "Monthly":
            first_of_month = current_time.replace(day=1)
            query += " WHERE date >= ?"
            params.append(first_of_month.strftime("%Y-%m-%d"))
        elif filter_option == "Yearly":
            first_of_year = current_time.replace(month=1, day=1)
            query += " WHERE date >= ?"
            params.append(first_of_year.strftime("%Y-%m-%d"))
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute(query, params)
            for row in c.fetchall():
                self.tree.insert("", "end", values=row)
    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
        query = "SELECT amount, category, payment_method, description, date FROM expenses"
        with sqlite3.connect(DB_NAME) as conn:
            df = pd.read_sql_query(query, conn)
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Export Successful", f"Expenses exported to {file_path}")
    def generate_graph(self):
        query = "SELECT category, SUM(amount) as total FROM expenses GROUP BY category"
        with sqlite3.connect(DB_NAME) as conn:
            df = pd.read_sql_query(query, conn)
        if df.empty:
            messagebox.showinfo("No Data", "No expenses to display.")
            return
        plt.figure(figsize=(8, 6), facecolor=BG_COLOR)
        plt.pie(df['total'], labels=df['category'], autopct='%1.1f%%', startangle=140, colors=[ACCENT_COLOR, "#6A5ACD", "#4169E1", "#483D8B", "#8A2BE2"],textprops={'color': 'white'})        
        plt.title("Expenses by Category", color=TEXT_COLOR)
        plt.show()
    def check_budget_alert(self):
        query = "SELECT SUM(amount) FROM expenses WHERE date >= ?"
        first_of_month = datetime.now().replace(day=1).strftime("%Y-%m-%d")
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute(query, (first_of_month,))
            total = c.fetchone()[0] or 0
        if total > BUDGET:
            messagebox.showwarning("Budget Alert", f"You have exceeded your monthly budget of {BUDGET}!")
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()