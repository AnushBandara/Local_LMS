# ui/edit_classes.py
import tkinter as tk
from tkinter import ttk, messagebox
from utils import styles
from db.database import get_all_classes, delete_class, add_new_class


# -------------------------------------------------------------------
# Edit Classes Page
# -------------------------------------------------------------------
def open_edit_classes(root, username, open_admin_dashboard_func):
    """Display list of classes with delete and add functionality."""
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
        text="Edit Classes",
        font=(styles.FONT_FAMILY, 26, "bold"),
        fg=styles.FG_COLOR,
        bg=styles.BG_COLOR
    ).pack(pady=(40, 30))

    # ----- Add Class Card -----
    add_card = tk.Frame(scroll_frame, bg=styles.ENTRY_BG, relief="flat", width=700, height=120)
    add_card.pack(pady=20)
    add_card.pack_propagate(False)

    tk.Label(
        add_card,
        text="➕ Add New Class",
        font=(styles.FONT_FAMILY, 18, "bold"),
        fg=styles.FG_COLOR,
        bg=styles.ENTRY_BG
    ).pack(pady=(15, 10))

    tk.Button(
        add_card,
        text="Open",
        command=lambda: open_add_class_page(root, username, open_admin_dashboard_func),
        font=(styles.FONT_FAMILY, 12, "bold"),
        bg=styles.BUTTON_PRIMARY,
        fg=styles.BG_COLOR,
        relief="flat",
        width=15,
        height=2,
        cursor="hand2"
    ).pack(pady=(0, 10))

    # ----- Load Classes -----
    classes = get_all_classes()

    if not classes:
        tk.Label(
            scroll_frame,
            text="No classes found in the database.",
            font=(styles.FONT_FAMILY, 14),
            fg=styles.FG_COLOR,
            bg=styles.BG_COLOR
        ).pack(pady=40)
        return

    for cname, grade in classes:
        card = tk.Frame(scroll_frame, bg=styles.ENTRY_BG, relief="flat", width=700, height=130)
        card.pack(pady=15)
        card.pack_propagate(False)

        info_text = f"🏫 {cname}   |   Grade: {grade}"

        tk.Label(
            card,
            text=info_text,
            font=(styles.FONT_FAMILY, 14),
            fg=styles.FG_COLOR,
            bg=styles.ENTRY_BG
        ).pack(pady=(20, 10))

        def confirm_delete(target=cname):
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the '{target}' class?"):
                delete_class(target)
                messagebox.showinfo("Deleted", f"Class '{target}' removed successfully.")
                open_edit_classes(root, username, open_admin_dashboard_func)

        tk.Button(
            card,
            text="Delete Class",
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
# Add Class Page (functional)
# -------------------------------------------------------------------
def open_add_class_page(root, username, open_admin_dashboard_func):
    """Add New Class Form Page."""
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg=styles.BG_COLOR)

    # Top bar
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
        command=lambda: open_edit_classes(root, username, open_admin_dashboard_func),
        font=(styles.FONT_FAMILY, 12, "bold"),
        bg=styles.BUTTON_PRIMARY,
        fg=styles.BG_COLOR,
        relief="flat",
        width=12,
        height=1,
        cursor="hand2"
    ).pack(side="right", padx=25, pady=10)

    # Scrollable form
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

    # Title
    tk.Label(
        scroll_frame,
        text="Add New Class",
        font=(styles.FONT_FAMILY, 26, "bold"),
        fg=styles.FG_COLOR,
        bg=styles.BG_COLOR
    ).pack(pady=(40, 20))

    # Class Name
    tk.Label(scroll_frame, text="Class Name:", font=styles.FONT_LABEL,
             fg=styles.FG_COLOR, bg=styles.BG_COLOR).pack()
    class_entry = tk.Entry(scroll_frame, font=styles.FONT_ENTRY, bg=styles.ENTRY_BG,
                           fg=styles.FG_COLOR, insertbackground=styles.FG_COLOR,
                           relief="flat", width=40, justify="center")
    class_entry.pack(pady=(5, 15), ipady=8)

    # Grade Selection
    tk.Label(scroll_frame, text="Grade:", font=styles.FONT_LABEL,
             fg=styles.FG_COLOR, bg=styles.BG_COLOR).pack()
    grade_var = tk.StringVar()
    grade_dropdown = ttk.Combobox(scroll_frame, textvariable=grade_var,
                                  values=["Grade 12", "Grade 13", "none"], state="readonly", width=37)
    grade_dropdown.pack(pady=(5, 25))
    grade_dropdown.set("Select Grade")

    # Save button
    def save_class():
        cname = class_entry.get().strip()
        grade = grade_var.get()

        if not cname or grade == "Select Grade":
            messagebox.showerror("Error", "All fields must be filled.")
            return

        if grade == "none":
            messagebox.showerror("Error", "A class must be assigned to Grade 12 or Grade 13.")
            return

        success = add_new_class(cname, grade)
        if success:
            messagebox.showinfo("Success", f"Class '{cname}' added successfully.")
            open_edit_classes(root, username, open_admin_dashboard_func)
        else:
            messagebox.showerror("Error", f"Class '{cname}' already exists.")

    tk.Button(
        scroll_frame,
        text="Save Class",
        command=save_class,
        font=(styles.FONT_FAMILY, 14, "bold"),
        bg=styles.BUTTON_PRIMARY,
        fg=styles.BG_COLOR,
        relief="flat",
        width=20,
        height=2,
        cursor="hand2"
    ).pack(pady=(10, 40))

    # Mouse scroll
    def _on_mousewheel(event):
        canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)