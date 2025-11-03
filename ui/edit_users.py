# ui/edit_users.py
import tkinter as tk
from tkinter import ttk, messagebox
from utils import styles
from db.database import get_all_users, delete_user, add_new_user


# -------------------------------------------------------------------
# Edit Users Page
# -------------------------------------------------------------------
def open_edit_users(root, username, open_admin_dashboard_func):
    """Display list of users with delete and add functionality."""
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg=styles.BG_COLOR)

    # ----- Top Bar -----
    top_frame = tk.Frame(root, bg=styles.ENTRY_BG, height=70)
    top_frame.pack(fill="x", side="top")

    tk.Label(
        top_frame,
        text=f"Logged in as: {username} (Admin)",
        font=(styles.FONT_FAMILY, 14),
        fg=styles.FG_COLOR,
        bg=styles.ENTRY_BG
    ).pack(side="left", padx=25, pady=10)

    tk.Button(
        top_frame,
        text="Back",
        command=lambda: open_admin_dashboard_func(root, username, None),
        font=(styles.FONT_FAMILY, 12, "bold"),
        bg=styles.BUTTON_PRIMARY,
        fg=styles.BG_COLOR,
        relief="flat",
        width=12,
        height=1,
        cursor="hand2"
    ).pack(side="right", padx=25, pady=10)

    # ----- Scrollable Main Area -----
    main_frame = tk.Frame(root, bg=styles.BG_COLOR)
    main_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(main_frame, bg=styles.BG_COLOR, highlightthickness=0)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=styles.BG_COLOR)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="n")
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ----- Title -----
    tk.Label(
        scroll_frame,
        text="Edit Users",
        font=(styles.FONT_FAMILY, 26, "bold"),
        fg=styles.FG_COLOR,
        bg=styles.BG_COLOR
    ).pack(pady=(40, 30))

    # ----- Add User Card -----
    add_card = tk.Frame(scroll_frame, bg=styles.ENTRY_BG, relief="flat", width=700, height=120)
    add_card.pack(pady=20)
    add_card.pack_propagate(False)

    tk.Label(
        add_card,
        text="➕ Add New User",
        font=(styles.FONT_FAMILY, 18, "bold"),
        fg=styles.FG_COLOR,
        bg=styles.ENTRY_BG
    ).pack(pady=(15, 10))

    tk.Button(
        add_card,
        text="Open",
        command=lambda: open_add_user_page(root, username, open_admin_dashboard_func),
        font=(styles.FONT_FAMILY, 12, "bold"),
        bg=styles.BUTTON_PRIMARY,
        fg=styles.BG_COLOR,
        relief="flat",
        width=15,
        height=2,
        cursor="hand2"
    ).pack(pady=(0, 10))

    # ----- Load Users -----
    users = get_all_users()

    if not users:
        tk.Label(
            scroll_frame,
            text="No users found in the database.",
            font=(styles.FONT_FAMILY, 14),
            fg=styles.FG_COLOR,
            bg=styles.BG_COLOR
        ).pack(pady=40)
        return

    for uname, status, grade in users:
        card = tk.Frame(scroll_frame, bg=styles.ENTRY_BG, relief="flat", width=700, height=130)
        card.pack(pady=15)
        card.pack_propagate(False)

        info_text = f"👤 {uname}   |   Role: {status}"
        if status == "student" and grade:
            info_text += f"   |   Grade: {grade}"

        tk.Label(
            card,
            text=info_text,
            font=(styles.FONT_FAMILY, 14),
            fg=styles.FG_COLOR,
            bg=styles.ENTRY_BG
        ).pack(pady=(20, 10))

        def confirm_delete(target=uname):
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{target}'?"):
                delete_user(target)
                messagebox.showinfo("Deleted", f"User '{target}' removed successfully.")
                open_edit_users(root, username, open_admin_dashboard_func)

        tk.Button(
            card,
            text="Delete User",
            command=confirm_delete,
            font=(styles.FONT_FAMILY, 12, "bold"),
            bg=styles.BUTTON_PRIMARY,
            fg=styles.BG_COLOR,
            relief="flat",
            width=14,
            height=1,
            cursor="hand2"
        ).pack()

    # Mouse scroll
    def _on_mousewheel(event):
        canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)


# -------------------------------------------------------------------
# Add User Page (functional)
# -------------------------------------------------------------------
def open_add_user_page(root, username, open_admin_dashboard_func):
    """Add New User Form Page."""
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg=styles.BG_COLOR)

    # ----- Top Bar -----
    top_frame = tk.Frame(root, bg=styles.ENTRY_BG, height=70)
    top_frame.pack(fill="x", side="top")

    tk.Label(
        top_frame,
        text=f"Logged in as: {username} (Admin)",
        font=(styles.FONT_FAMILY, 14),
        fg=styles.FG_COLOR,
        bg=styles.ENTRY_BG
    ).pack(side="left", padx=25, pady=10)

    tk.Button(
        top_frame,
        text="Back",
        command=lambda: open_edit_users(root, username, open_admin_dashboard_func),
        font=(styles.FONT_FAMILY, 12, "bold"),
        bg=styles.BUTTON_PRIMARY,
        fg=styles.BG_COLOR,
        relief="flat",
        width=12,
        height=1,
        cursor="hand2"
    ).pack(side="right", padx=25, pady=10)

    # ----- Scrollable Content -----
    main_frame = tk.Frame(root, bg=styles.BG_COLOR)
    main_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(main_frame, bg=styles.BG_COLOR, highlightthickness=0)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=styles.BG_COLOR)
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="n")
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ----- Title -----
    tk.Label(
        scroll_frame,
        text="Add New User",
        font=(styles.FONT_FAMILY, 26, "bold"),
        fg=styles.FG_COLOR,
        bg=styles.BG_COLOR
    ).pack(pady=(40, 20))

    # ----- Username -----
    tk.Label(
        scroll_frame,
        text="Username:",
        font=styles.FONT_LABEL,
        fg=styles.FG_COLOR,
        bg=styles.BG_COLOR
    ).pack()
    username_entry = tk.Entry(scroll_frame, font=styles.FONT_ENTRY, bg=styles.ENTRY_BG,
                              fg=styles.FG_COLOR, insertbackground=styles.FG_COLOR, relief="flat", width=40, justify="center")
    username_entry.pack(pady=(5, 15), ipady=8)

    # ----- Password -----
    tk.Label(scroll_frame, text="Password:", font=styles.FONT_LABEL,
             fg=styles.FG_COLOR, bg=styles.BG_COLOR).pack()
    password_entry = tk.Entry(scroll_frame, show="*", font=styles.FONT_ENTRY, bg=styles.ENTRY_BG,
                              fg=styles.FG_COLOR, insertbackground=styles.FG_COLOR, relief="flat", width=40, justify="center")
    password_entry.pack(pady=(5, 15), ipady=8)

    # ----- Confirm Password -----
    tk.Label(scroll_frame, text="Re-enter Password:", font=styles.FONT_LABEL,
             fg=styles.FG_COLOR, bg=styles.BG_COLOR).pack()
    confirm_password_entry = tk.Entry(scroll_frame, show="*", font=styles.FONT_ENTRY, bg=styles.ENTRY_BG,
                                      fg=styles.FG_COLOR, insertbackground=styles.FG_COLOR, relief="flat", width=40, justify="center")
    confirm_password_entry.pack(pady=(5, 15), ipady=8)

    # ----- Role Selection -----
    tk.Label(scroll_frame, text="Role:", font=styles.FONT_LABEL,
             fg=styles.FG_COLOR, bg=styles.BG_COLOR).pack()
    role_var = tk.StringVar()
    role_dropdown = ttk.Combobox(scroll_frame, textvariable=role_var, values=["admin", "student"], state="readonly", width=37)
    role_dropdown.pack(pady=(5, 15))
    role_dropdown.set("Select Role")

    # ----- Grade Selection -----
    tk.Label(scroll_frame, text="Grade:", font=styles.FONT_LABEL,
             fg=styles.FG_COLOR, bg=styles.BG_COLOR).pack()
    grade_var = tk.StringVar()
    grade_dropdown = ttk.Combobox(scroll_frame, textvariable=grade_var, values=["Grade 12", "Grade 13", "none"], state="readonly", width=37)
    grade_dropdown.pack(pady=(5, 25))
    grade_dropdown.set("Select Grade")

    # ----- Save Button -----
    def save_user():
        uname = username_entry.get().strip()
        pw = password_entry.get().strip()
        confirm_pw = confirm_password_entry.get().strip()
        role = role_var.get()
        grade = grade_var.get()

        if not uname or not pw or not confirm_pw or role == "Select Role" or grade == "Select Grade":
            messagebox.showerror("Error", "All fields must be filled.")
            return

        if pw != confirm_pw:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        if role == "student" and grade not in ["Grade 12", "Grade 13"]:
            messagebox.showerror("Error", "Students must be assigned to Grade 12 or Grade 13.")
            return

        if role == "admin" and grade != "none":
            messagebox.showerror("Error", "Admins must have grade set to 'none'.")
            return

        success = add_new_user(uname, pw, role, None if grade == "none" else grade)
        if success:
            messagebox.showinfo("Success", f"User '{uname}' added successfully.")
            open_edit_users(root, username, open_admin_dashboard_func)
        else:
            messagebox.showerror("Error", f"Username '{uname}' already exists.")

    tk.Button(
        scroll_frame,
        text="Save User",
        command=save_user,
        font=(styles.FONT_FAMILY, 14, "bold"),
        bg=styles.BUTTON_PRIMARY,
        fg=styles.BG_COLOR,
        relief="flat",
        width=20,
        height=2,
        cursor="hand2"
    ).pack(pady=(10, 40))

    def _on_mousewheel(event):
        canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)