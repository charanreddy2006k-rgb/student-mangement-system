"""
main.py
-------
Student Management System – Tkinter GUI.

Run this file to start the application:
    python main.py

The window has:
- A left navigation (Dashboard, Students, Add Student, Statistics)
- A right content area that changes when you click a menu button
"""

import tkinter as tk
from tkinter import ttk, messagebox

import database
from student import empty_student, validate_student


# Simple colour palette (easy to change for viva / screenshots)
COLORS = {
    "bg": "#F4F7FB",
    "sidebar": "#1B3A4B",
    "sidebar_hover": "#24556B",
    "accent": "#2A9D8F",
    "accent_dark": "#21867A",
    "danger": "#E76F51",
    "card": "#FFFFFF",
    "text": "#1B3A4B",
    "muted": "#5C6B73",
    "header": "#0E2A3A",
}

DEPARTMENTS = (
    "Computer Science",
    "Electronics",
    "Electrical",
    "Mechanical",
    "Civil",
    "Information Technology",
)

SEMESTERS = ("1", "2", "3", "4", "5", "6", "7", "8")
GENDERS = ("Male", "Female", "Other")


class StudentManagementApp:
    """Main window of the Student Management System."""

    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1100x680")
        self.root.minsize(980, 600)
        self.root.configure(bg=COLORS["bg"])

        # Remember which student is selected in the table
        self.selected_student_id = None
        # Remember if we are adding a new student or editing an existing one
        self.form_mode = "add"

        database.initialize_database()
        self._setup_style()
        self._build_layout()
        self.show_dashboard()

    def _setup_style(self):
        """Make ttk widgets look a bit more modern."""
        style = ttk.Style()
        # 'clam' works well on Windows for custom colours
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            background=COLORS["card"],
            foreground=COLORS["text"],
            rowheight=28,
            fieldbackground=COLORS["card"],
            font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading",
            background=COLORS["header"],
            foreground="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
        )
        style.map("Treeview.Heading", background=[("active", COLORS["sidebar"])])
        style.map("Treeview", background=[("selected", COLORS["accent"])])

        style.configure("TCombobox", padding=4, font=("Segoe UI", 10))

    def _build_layout(self):
        """Create sidebar + main content area."""
        self.sidebar = tk.Frame(self.root, bg=COLORS["sidebar"], width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        title = tk.Label(
            self.sidebar,
            text="SMS",
            bg=COLORS["sidebar"],
            fg="#FFFFFF",
            font=("Segoe UI", 22, "bold"),
        )
        title.pack(pady=(28, 0))

        subtitle = tk.Label(
            self.sidebar,
            text="Student Management",
            bg=COLORS["sidebar"],
            fg="#A8C5D4",
            font=("Segoe UI", 10),
        )
        subtitle.pack(pady=(0, 24))

        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "Dashboard"),
            ("students", "All Students"),
            ("add", "Add Student"),
            ("stats", "Statistics"),
        ]
        for key, label in nav_items:
            btn = tk.Button(
                self.sidebar,
                text=label,
                font=("Segoe UI", 11),
                bg=COLORS["sidebar"],
                fg="#FFFFFF",
                activebackground=COLORS["sidebar_hover"],
                activeforeground="#FFFFFF",
                bd=0,
                relief="flat",
                cursor="hand2",
                anchor="w",
                padx=24,
                pady=12,
                command=lambda k=key: self._on_nav(k),
            )
            btn.pack(fill="x")
            self.nav_buttons[key] = btn

        footer = tk.Label(
            self.sidebar,
            text="3rd Semester Mini Project",
            bg=COLORS["sidebar"],
            fg="#7FA3B5",
            font=("Segoe UI", 8),
        )
        footer.pack(side="bottom", pady=16)

        self.content = tk.Frame(self.root, bg=COLORS["bg"])
        self.content.pack(side="right", fill="both", expand=True)

    def _on_nav(self, key):
        """Handle left-menu clicks."""
        if key == "dashboard":
            self.show_dashboard()
        elif key == "students":
            self.show_students()
        elif key == "add":
            self.show_student_form(mode="add")
        elif key == "stats":
            self.show_statistics()

    def _highlight_nav(self, active_key):
        for key, btn in self.nav_buttons.items():
            if key == active_key:
                btn.configure(bg=COLORS["accent"])
            else:
                btn.configure(bg=COLORS["sidebar"])

    def _clear_content(self):
        """Remove whatever page is currently shown."""
        for widget in self.content.winfo_children():
            widget.destroy()

    def _page_header(self, parent, title, subtitle):
        header = tk.Frame(parent, bg=COLORS["bg"])
        header.pack(fill="x", padx=28, pady=(22, 8))
        tk.Label(
            header,
            text=title,
            bg=COLORS["bg"],
            fg=COLORS["header"],
            font=("Segoe UI", 20, "bold"),
        ).pack(anchor="w")
        tk.Label(
            header,
            text=subtitle,
            bg=COLORS["bg"],
            fg=COLORS["muted"],
            font=("Segoe UI", 10),
        ).pack(anchor="w")
        return header

    def _card(self, parent, **pack_options):
        card = tk.Frame(parent, bg=COLORS["card"], highlightthickness=1, highlightbackground="#D9E2EC")
        card.pack(**pack_options)
        return card

    # ------------------------------------------------------------------
    # Dashboard
    # ------------------------------------------------------------------
    def show_dashboard(self):
        self._highlight_nav("dashboard")
        self._clear_content()
        self._page_header(
            self.content,
            "Dashboard",
            "Welcome to the Student Management System",
        )

        total, by_dept = database.get_statistics()

        cards_row = tk.Frame(self.content, bg=COLORS["bg"])
        cards_row.pack(fill="x", padx=28, pady=12)

        self._stat_card(cards_row, "Total Students", str(total), COLORS["accent"]).pack(
            side="left", padx=(0, 12), ipadx=18, ipady=14
        )
        dept_count = str(len(by_dept))
        self._stat_card(cards_row, "Departments", dept_count, "#3D5A80").pack(
            side="left", padx=12, ipadx=18, ipady=14
        )
        self._stat_card(cards_row, "Sample Data", "Loaded on first run", "#E9C46A").pack(
            side="left", padx=12, ipadx=18, ipady=14
        )

        actions = self._card(self.content, fill="x", padx=28, pady=10)
        tk.Label(
            actions,
            text="Quick actions",
            bg=COLORS["card"],
            fg=COLORS["text"],
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", padx=16, pady=(14, 8))

        btn_row = tk.Frame(actions, bg=COLORS["card"])
        btn_row.pack(anchor="w", padx=16, pady=(0, 16))
        self._action_button(btn_row, "View Students", self.show_students, COLORS["accent"]).pack(
            side="left", padx=(0, 10)
        )
        self._action_button(btn_row, "Add Student", lambda: self.show_student_form("add"), COLORS["header"]).pack(
            side="left", padx=10
        )
        self._action_button(btn_row, "Statistics", self.show_statistics, "#3D5A80").pack(
            side="left", padx=10
        )

        recent = self._card(self.content, fill="both", expand=True, padx=28, pady=(6, 20))
        tk.Label(
            recent,
            text="Recent students",
            bg=COLORS["card"],
            fg=COLORS["text"],
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", padx=16, pady=(14, 6))
        self._build_table(recent, database.get_all_students()[:6], compact=True)

    def _stat_card(self, parent, title, value, accent):
        frame = tk.Frame(parent, bg=COLORS["card"], highlightthickness=1, highlightbackground="#D9E2EC")
        bar = tk.Frame(frame, bg=accent, width=6)
        bar.pack(side="left", fill="y")
        inner = tk.Frame(frame, bg=COLORS["card"])
        inner.pack(side="left", padx=14, pady=8)
        tk.Label(inner, text=title, bg=COLORS["card"], fg=COLORS["muted"], font=("Segoe UI", 9)).pack(anchor="w")
        tk.Label(inner, text=value, bg=COLORS["card"], fg=COLORS["text"], font=("Segoe UI", 16, "bold")).pack(
            anchor="w"
        )
        return frame

    def _action_button(self, parent, text, command, color):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="#FFFFFF",
            activebackground=COLORS["accent_dark"],
            activeforeground="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            padx=14,
            pady=8,
            cursor="hand2",
        )

    # ------------------------------------------------------------------
    # Students table (view / search / update / delete)
    # ------------------------------------------------------------------
    def show_students(self, keyword=None):
        self._highlight_nav("students")
        self._clear_content()
        self._page_header(
            self.content,
            "All Students",
            "Search, update, or delete student records",
        )

        toolbar = tk.Frame(self.content, bg=COLORS["bg"])
        toolbar.pack(fill="x", padx=28, pady=(4, 8))

        tk.Label(
            toolbar,
            text="Search by Student ID or Name:",
            bg=COLORS["bg"],
            fg=COLORS["text"],
            font=("Segoe UI", 10),
        ).pack(side="left")

        self.search_var = tk.StringVar(value=keyword or "")
        search_entry = tk.Entry(
            toolbar,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            width=28,
            relief="solid",
            bd=1,
        )
        search_entry.pack(side="left", padx=8, ipady=4)
        search_entry.bind("<Return>", lambda _e: self._run_search())

        self._action_button(toolbar, "Search", self._run_search, COLORS["accent"]).pack(side="left", padx=4)
        self._action_button(toolbar, "Show All", self.show_students, COLORS["header"]).pack(side="left", padx=4)
        self._action_button(
            toolbar, "Add New", lambda: self.show_student_form("add"), COLORS["accent"]
        ).pack(side="right")

        table_card = self._card(self.content, fill="both", expand=True, padx=28, pady=(0, 8))
        records = database.search_students(self.search_var.get())
        self._build_table(table_card, records)

        buttons = tk.Frame(self.content, bg=COLORS["bg"])
        buttons.pack(fill="x", padx=28, pady=(0, 18))
        self._action_button(buttons, "Update Selected", self._update_selected, COLORS["header"]).pack(
            side="left", padx=(0, 8)
        )
        tk.Button(
            buttons,
            text="Delete Selected",
            command=self._delete_selected,
            bg=COLORS["danger"],
            fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            padx=14,
            pady=8,
            cursor="hand2",
        ).pack(side="left")

        tk.Label(
            buttons,
            text="Tip: click a row first, then Update or Delete.",
            bg=COLORS["bg"],
            fg=COLORS["muted"],
            font=("Segoe UI", 9),
        ).pack(side="left", padx=14)

    def _run_search(self):
        keyword = self.search_var.get().strip()
        self.show_students(keyword=keyword)

    def _build_table(self, parent, records, compact=False):
        columns = ("student_id", "name", "age", "gender", "department", "semester", "phone", "email")
        headings = {
            "student_id": "Student ID",
            "name": "Name",
            "age": "Age",
            "gender": "Gender",
            "department": "Department",
            "semester": "Sem",
            "phone": "Phone",
            "email": "Email",
        }

        frame = tk.Frame(parent, bg=COLORS["card"])
        frame.pack(fill="both", expand=True, padx=12, pady=12)

        tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        widths = {
            "student_id": 100,
            "name": 150,
            "age": 50,
            "gender": 80,
            "department": 150,
            "semester": 50,
            "phone": 110,
            "email": 200,
        }
        for col in columns:
            tree.heading(col, text=headings[col])
            tree.column(col, width=widths[col], anchor="w", minwidth=50)

        for row in records:
            tree.insert(
                "",
                "end",
                values=(
                    row["student_id"],
                    row["name"],
                    row["age"],
                    row["gender"],
                    row["department"],
                    row["semester"],
                    row["phone"],
                    row["email"],
                ),
            )

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        if not compact:
            hsb.grid(row=1, column=0, sticky="ew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        if not records:
            tk.Label(
                frame,
                text="No student records found.",
                bg=COLORS["card"],
                fg=COLORS["muted"],
                font=("Segoe UI", 10),
            ).place(relx=0.5, rely=0.5, anchor="center")

        tree.bind("<<TreeviewSelect>>", lambda _e: self._on_row_select(tree))
        tree.bind("<Double-1>", lambda _e: self._update_selected())
        self.tree = tree

        count_text = f"Showing {len(records)} student(s)"
        tk.Label(
            parent,
            text=count_text,
            bg=COLORS["card"],
            fg=COLORS["muted"],
            font=("Segoe UI", 9),
        ).pack(anchor="e", padx=16, pady=(0, 10))

    def _on_row_select(self, tree):
        selected = tree.selection()
        if not selected:
            self.selected_student_id = None
            return
        values = tree.item(selected[0], "values")
        self.selected_student_id = values[0] if values else None

    def _update_selected(self):
        if not self.selected_student_id:
            messagebox.showwarning("No student selected", "Please select a student from the table first.")
            return
        self.show_student_form(mode="update", student_id=self.selected_student_id)

    def _delete_selected(self):
        if not self.selected_student_id:
            messagebox.showwarning("No student selected", "Please select a student from the table first.")
            return

        student = database.get_student_by_id(self.selected_student_id)
        if not student:
            messagebox.showerror("Not found", "This student could not be found.")
            return

        confirm = messagebox.askyesno(
            "Confirm delete",
            f"Delete this student?\n\n"
            f"ID: {student['student_id']}\n"
            f"Name: {student['name']}\n\n"
            "This cannot be undone.",
        )
        if not confirm:
            return

        ok, message = database.delete_student(self.selected_student_id)
        if ok:
            self.selected_student_id = None
            messagebox.showinfo("Deleted", message)
            self.show_students()
        else:
            messagebox.showerror("Error", message)

    # ------------------------------------------------------------------
    # Add / Update form
    # ------------------------------------------------------------------
    def show_student_form(self, mode="add", student_id=None):
        self.form_mode = mode
        self._highlight_nav("add" if mode == "add" else "students")
        self._clear_content()

        if mode == "add":
            self._page_header(self.content, "Add Student", "Enter details and click Save")
            data = empty_student()
            self.editing_original_id = None
        else:
            self._page_header(self.content, "Update Student", "Change the fields and click Save")
            data = database.get_student_by_id(student_id) or empty_student()
            self.editing_original_id = student_id

        form_card = self._card(self.content, fill="both", expand=True, padx=28, pady=(4, 20))
        form = tk.Frame(form_card, bg=COLORS["card"])
        form.pack(padx=24, pady=20, anchor="nw")

        self.form_vars = {}
        left = tk.Frame(form, bg=COLORS["card"])
        right = tk.Frame(form, bg=COLORS["card"])
        left.grid(row=0, column=0, sticky="nw", padx=(0, 36))
        right.grid(row=0, column=1, sticky="nw")

        self._labeled_entry(left, "Student ID *", "student_id", data["student_id"], 0)
        self._labeled_entry(left, "Name *", "name", data["name"], 1)
        self._labeled_entry(left, "Age *", "age", str(data["age"]) if data["age"] else "", 2)
        self._labeled_combo(left, "Gender *", "gender", GENDERS, data["gender"], 3)

        self._labeled_combo(right, "Department *", "department", DEPARTMENTS, data["department"], 0)
        self._labeled_combo(right, "Semester *", "semester", SEMESTERS, str(data["semester"]) if data["semester"] else "", 1)
        self._labeled_entry(right, "Phone Number *", "phone", data["phone"], 2)
        self._labeled_entry(right, "Email *", "email", data["email"], 3)

        btn_row = tk.Frame(form, bg=COLORS["card"])
        btn_row.grid(row=1, column=0, columnspan=2, sticky="w", pady=(18, 0))

        save_text = "Save Student" if mode == "add" else "Save Changes"
        self._action_button(btn_row, save_text, self._save_form, COLORS["accent"]).pack(side="left", padx=(0, 8))
        self._action_button(btn_row, "Clear Form", self._clear_form, "#8D99AE").pack(side="left", padx=8)
        self._action_button(btn_row, "Back to List", self.show_students, COLORS["header"]).pack(side="left", padx=8)

        tk.Label(
            form,
            text="* Required fields. Phone must be 10 digits. Email needs an @ and a domain.",
            bg=COLORS["card"],
            fg=COLORS["muted"],
            font=("Segoe UI", 9),
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(14, 0))

    def _labeled_entry(self, parent, label, key, value, row):
        tk.Label(parent, text=label, bg=COLORS["card"], fg=COLORS["text"], font=("Segoe UI", 10)).grid(
            row=row * 2, column=0, sticky="w", pady=(8, 2)
        )
        var = tk.StringVar(value=value)
        entry = tk.Entry(parent, textvariable=var, font=("Segoe UI", 10), width=32, relief="solid", bd=1)
        entry.grid(row=row * 2 + 1, column=0, sticky="w", ipady=5)
        self.form_vars[key] = var

    def _labeled_combo(self, parent, label, key, values, current, row):
        tk.Label(parent, text=label, bg=COLORS["card"], fg=COLORS["text"], font=("Segoe UI", 10)).grid(
            row=row * 2, column=0, sticky="w", pady=(8, 2)
        )
        var = tk.StringVar(value=current)
        combo = ttk.Combobox(parent, textvariable=var, values=values, state="readonly", width=30)
        combo.grid(row=row * 2 + 1, column=0, sticky="w", ipady=2)
        self.form_vars[key] = var

    def _clear_form(self):
        for key, var in self.form_vars.items():
            var.set("")

    def _save_form(self):
        raw = {key: var.get() for key, var in self.form_vars.items()}
        ok, result = validate_student(raw, is_update=(self.form_mode == "update"))
        if not ok:
            messagebox.showerror("Validation error", result)
            return

        if self.form_mode == "add":
            saved, message = database.add_student(result)
        else:
            saved, message = database.update_student(self.editing_original_id, result)

        if saved:
            messagebox.showinfo("Success", message)
            self.selected_student_id = result["student_id"].upper()
            self.show_students()
        else:
            messagebox.showerror("Could not save", message)

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------
    def show_statistics(self):
        self._highlight_nav("stats")
        self._clear_content()
        self._page_header(
            self.content,
            "Student Statistics",
            "Total students and department-wise count",
        )

        total, by_dept = database.get_statistics()

        top = tk.Frame(self.content, bg=COLORS["bg"])
        top.pack(fill="x", padx=28, pady=8)
        self._stat_card(top, "Total Students", str(total), COLORS["accent"]).pack(
            side="left", ipadx=20, ipady=16
        )

        table_card = self._card(self.content, fill="both", expand=True, padx=28, pady=(8, 20))
        tk.Label(
            table_card,
            text="Students department-wise",
            bg=COLORS["card"],
            fg=COLORS["text"],
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", padx=16, pady=(16, 8))

        frame = tk.Frame(table_card, bg=COLORS["card"])
        frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        columns = ("department", "count")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
        tree.heading("department", text="Department")
        tree.heading("count", text="Number of Students")
        tree.column("department", width=280, anchor="w")
        tree.column("count", width=180, anchor="center")

        if by_dept:
            for department, count in by_dept:
                tree.insert("", "end", values=(department, count))
        else:
            tree.insert("", "end", values=("No records yet", "0"))

        tree.pack(fill="both", expand=True)

        tk.Label(
            table_card,
            text="These numbers update automatically when you add or delete students.",
            bg=COLORS["card"],
            fg=COLORS["muted"],
            font=("Segoe UI", 9),
        ).pack(anchor="w", padx=16, pady=(0, 14))


def main():
    root = tk.Tk()
    StudentManagementApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
