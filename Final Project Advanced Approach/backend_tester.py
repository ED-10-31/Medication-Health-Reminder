import tkinter as tk
import os
from tkinter import ttk, messagebox

# These imports work for both JSON and SQLModel versions
# provided the function names in those files match (which they do in my examples).
from database import init_db
from auth import login_user, register_user
from medication import add_medication, get_user_medications, take_medication
from exporter import generate_pdf_report


class BackendTesterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Backend Logic Tester (Universal)")
        self.root.geometry("650x550")

        self.current_user_id = None

        # Initialize the Database (SQL or JSON depending on your backend files)
        init_db()

        # --- FRAMES ---
        self.login_frame = tk.Frame(self.root, padx=20, pady=20)
        self.dashboard_frame = tk.Frame(self.root, padx=10, pady=10)

        self.show_login()

    # ==========================
    #       LOGIN / AUTH
    # ==========================
    def show_login(self):
        self.dashboard_frame.pack_forget()
        self.login_frame.pack(fill='both', expand=True)

        # Clear previous widgets
        for widget in self.login_frame.winfo_children():
            widget.destroy()

        tk.Label(self.login_frame, text="Backend Login", font=("Times", 16, "bold")).pack(pady=10)

        tk.Label(self.login_frame, text="Username:").pack()
        self.entry_user = tk.Entry(self.login_frame)
        self.entry_user.pack()

        tk.Label(self.login_frame, text="Password:").pack()
        self.entry_pass = tk.Entry(self.login_frame, show="*")
        self.entry_pass.pack()

        btn_frame = tk.Frame(self.login_frame)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Login", width=10, command=self.do_login).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Register", width=10, command=self.do_register).pack(side='left', padx=5)

    def do_login(self):
        u = self.entry_user.get()
        p = self.entry_pass.get()
        user_id = login_user(u, p)

        if user_id:
            self.current_user_id = user_id
            messagebox.showinfo("Success", f"Logged in as User ID: {user_id}")
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def do_register(self):
        u = self.entry_user.get()
        p = self.entry_pass.get()
        if not u or not p:
            messagebox.showwarning("Warning", "Fields cannot be empty")
            return

        if register_user(u, p):
            messagebox.showinfo("Success", "User registered! You can now login.")
        else:
            messagebox.showerror("Error", "Username taken.")

    # ==========================
    #       DASHBOARD
    # ==========================
    def show_dashboard(self):
        self.login_frame.pack_forget()
        self.dashboard_frame.pack(fill='both', expand=True)

        # Clear previous widgets
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        # Header
        header = tk.Frame(self.dashboard_frame)
        header.pack(fill='x', pady=5)
        tk.Label(header, text=f"User ID: {self.current_user_id}", font=("Arial", 10, "bold")).pack(side='left')
        tk.Button(header, text="Logout", command=self.logout).pack(side='right')

        # --- SECTION: ADD MEDICATION ---
        add_frame = tk.LabelFrame(self.dashboard_frame, text="1. Add Medication", padx=5, pady=5)
        add_frame.pack(fill='x', pady=5)

        tk.Label(add_frame, text="Name:").grid(row=0, column=0)
        self.med_name_var = tk.Entry(add_frame, width=15)
        self.med_name_var.grid(row=0, column=1)

        tk.Label(add_frame, text="Total Pills:").grid(row=0, column=2)
        self.med_total_var = tk.Entry(add_frame, width=5)
        self.med_total_var.grid(row=0, column=3)

        tk.Label(add_frame, text="Per Day:").grid(row=0, column=4)
        self.med_daily_var = tk.Entry(add_frame, width=5)
        self.med_daily_var.grid(row=0, column=5)

        tk.Button(add_frame, text="Add", command=self.run_add_med).grid(row=0, column=6, padx=10)

        # --- SECTION: LIST & TAKE ---
        list_frame = tk.LabelFrame(self.dashboard_frame, text="2. Smart Refill & Actions", padx=5, pady=5)
        list_frame.pack(fill='both', expand=True, pady=5)

        # Columns for the Treeview
        cols = ("ID", "Name", "Stock", "Daily", "Days Left", "Status")
        self.tree = ttk.Treeview(list_frame, columns=cols, show='headings', height=8)

        for col in cols:
            self.tree.heading(col, text=col)
            # Adjust widths
            w = 150 if col == "Status" else 60
            if col == "Name": w = 120
            self.tree.column(col, width=w)

        self.tree.pack(fill='both', expand=True)

        action_frame = tk.Frame(list_frame)
        action_frame.pack(fill='x', pady=5)

        tk.Button(action_frame, text="Take Selected Med", bg="#ddffdd", command=self.run_take_med).pack(side='left',
                                                                                                        fill='x',
                                                                                                        expand=True,
                                                                                                        padx=2)
        tk.Button(action_frame, text="Refresh List", command=self.refresh_list).pack(side='left', fill='x', expand=True,
                                                                                     padx=2)

        # --- SECTION: EXPORT ---
        export_frame = tk.LabelFrame(self.dashboard_frame, text="3. Reporting", padx=5, pady=5)
        export_frame.pack(fill='x', pady=5)

        tk.Button(export_frame, text="Generate PDF Report (Times New Roman)", command=self.run_export).pack(fill='x')

        # Load initial data
        self.refresh_list()

    def logout(self):
        self.current_user_id = None
        self.show_login()

    # --- FUNCTION CONNECTORS ---
    def refresh_list(self):
        # Clear list
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get data from YOUR BACKEND
        meds = get_user_medications(self.current_user_id)

        for m in meds:
            # --- UNIVERSAL HELPER ---
            # This allows the GUI to work whether 'm' is a Dictionary (JSON mode)
            # OR a SQLModel Object (SQL mode)
            def get_val(key):
                if isinstance(m, dict):
                    return m.get(key)
                return getattr(m, key, None)

            m_id = get_val('id')
            m_name = get_val('name')
            m_stock = get_val('total_pills')  # SQLModel uses total_pills
            if m_stock is None: m_stock = get_val('stock')  # Fallback if JSON uses 'stock'

            m_daily = get_val('pills_per_day')
            m_days = get_val('days_remaining')
            m_alert = get_val('alert')

            status = "OK"
            # Visual check for low stock
            if m_alert:
                status = "⚠️ LOW STOCK"

            # Insert into GUI
            self.tree.insert("", "end", values=(
                m_id,
                m_name,
                m_stock,
                m_daily,
                m_days,
                status
            ))

    def run_add_med(self):
        name = self.med_name_var.get()
        total = self.med_total_var.get()
        daily = self.med_daily_var.get()

        if not name or not total or not daily:
            messagebox.showwarning("Input", "Please fill all fields")
            return

        try:
            # Call YOUR BACKEND function
            add_medication(self.current_user_id, name, int(total), int(daily))
            # Clear inputs
            self.med_name_var.delete(0, tk.END)
            self.med_total_var.delete(0, tk.END)
            self.med_daily_var.delete(0, tk.END)
            self.refresh_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_take_med(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Please select a medication from the list first.")
            return

        item = self.tree.item(selected)
        med_id = item['values'][0]
        med_name = item['values'][1]

        # Call YOUR BACKEND function
        success, new_stock = take_medication(med_id, 1)

        if success:
            messagebox.showinfo("Taken", f"Took 1 {med_name}. New Stock: {new_stock}")
            self.refresh_list()
        else:
            messagebox.showerror("Error", "Could not take medication.")

    def run_export(self):
        # Define the folder name
        folder_name = "Medication_Reports"

        # Create the folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Construct the full path (Folder + Filename)
        filename = f"Report_User_{self.current_user_id}.pdf"
        full_path = os.path.join(folder_name, filename)

        if generate_pdf_report(self.current_user_id, full_path):
            # Get absolute path to show user exactly where it is
            abs_path = os.path.abspath(full_path)
            messagebox.showinfo("Export", f"PDF Created Successfully!\n\nSaved at:\n{abs_path}")
        else:
            messagebox.showerror("Export", "Failed to create PDF (Check console for details)")


if __name__ == "__main__":
    root = tk.Tk()
    app = BackendTesterApp(root)
    root.mainloop()
