# ui/edit_topics.py
import tkinter as tk
from tkinter import ttk, messagebox
from utils import styles
from db.database import get_all_topics, delete_topic, get_all_class_names, add_new_topic


# -------------------------------------------------------------------
# Edit Topics Page
# -------------------------------------------------------------------
def open_edit_topics(root, username, open_admin_dashboard_func):
    """Display list of topics with delete and add functionality."""
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
        text="Edit Topics",
        font=(styles.FONT_FAMILY, 26, "bold"),
        fg=styles.FG_COLOR,
        bg=styles.BG_COLOR
    ).pack(pady=(40, 30))

    # ----- Add Topic Card -----
    add_card = tk.Frame(scroll_frame, bg=styles.ENTRY_BG, relief="flat", width=700, height=120)
    add_card.pack(pady=20)
    add_card.pack_propagate(False)

    tk.Label(
        add_card,
        text="➕ Add New Topic",
        font=(styles.FONT_FAMILY, 18, "bold"),
        fg=styles.FG_COLOR,
        bg=styles.ENTRY_BG
    ).pack(pady=(15, 10))

    tk.Button(
        add_card,
        text="Open",
        command=lambda: open_add_topic_page(root, username, open_admin_dashboard_func),
        font=(styles.FONT_FAMILY, 12, "bold"),
        bg=styles.BUTTON_PRIMARY,
        fg=styles.BG_COLOR,
        relief="flat",
        width=15,
        height=2,
        cursor="hand2"
    ).pack(pady=(0, 10))

    # ----- Load Topics -----
    topics = get_all_topics()

    if not topics:
        tk.Label(
            scroll_frame,
            text="No topics found in the database.",
            font=(styles.FONT_FAMILY, 14),
            fg=styles.FG_COLOR,
            bg=styles.BG_COLOR
        ).pack(pady=40)
        return

    for topic_name, class_name in topics:
        card = tk.Frame(scroll_frame, bg=styles.ENTRY_BG, relief="flat", width=700, height=130)
        card.pack(pady=15)
        card.pack_propagate(False)

        info_text = f"📘 {topic_name}   |   Class: {class_name}"

        tk.Label(
            card,
            text=info_text,
            font=(styles.FONT_FAMILY, 14),
            fg=styles.FG_COLOR,
            bg=styles.ENTRY_BG
        ).pack(pady=(20, 10))

        def confirm_delete(target_t=topic_name, target_c=class_name):
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the '{target_t}' topic from '{target_c}'?"):
                delete_topic(target_t, target_c)
                messagebox.showinfo("Deleted", f"Topic '{target_t}' from '{target_c}' removed successfully.")
                open_edit_topics(root, username, open_admin_dashboard_func)

        tk.Button(
            card,
            text="Delete Topic",
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
# Add Topic Page (Functional)
# -------------------------------------------------------------------
def open_add_topic_page(root, username, open_admin_dashboard_func):
    """Add New Topic Form Page."""
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
        command=lambda: open_edit_topics(root, username, open_admin_dashboard_func),
        font=(styles.FONT_FAMILY, 12, "bold"),
        bg=styles.BUTTON_PRIMARY,
        fg=styles.BG_COLOR,
        relief="flat",
        width=12,
        height=1,
        cursor="hand2"
    ).pack(side="right", padx=25, pady=10)

    # ----- Scrollable Form -----
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
        text="Add New Topic",
        font=(styles.FONT_FAMILY, 26, "bold"),
        fg=styles.FG_COLOR,
        bg=styles.BG_COLOR
    ).pack(pady=(40, 20))

    # ----- Topic Name -----
    tk.Label(scroll_frame, text="Topic Name:", font=styles.FONT_LABEL,
             fg=styles.FG_COLOR, bg=styles.BG_COLOR).pack()
    topic_entry = tk.Entry(scroll_frame, font=styles.FONT_ENTRY, bg=styles.ENTRY_BG,
                           fg=styles.FG_COLOR, insertbackground=styles.FG_COLOR,
                           relief="flat", width=40, justify="center")
    topic_entry.pack(pady=(5, 15), ipady=8)

    # ----- Class Selection -----
    tk.Label(scroll_frame, text="Select Class:", font=styles.FONT_LABEL,
             fg=styles.FG_COLOR, bg=styles.BG_COLOR).pack()
    class_var = tk.StringVar()
    class_list = get_all_class_names()
    class_dropdown = ttk.Combobox(scroll_frame, textvariable=class_var, values=class_list, state="readonly", width=37)
    class_dropdown.pack(pady=(5, 25))
    class_dropdown.set("Select Class")

    # ----- Description -----
    tk.Label(scroll_frame, text="Topic Description:", font=styles.FONT_LABEL,
             fg=styles.FG_COLOR, bg=styles.BG_COLOR).pack()
    desc_entry = tk.Text(scroll_frame, font=styles.FONT_ENTRY, bg=styles.ENTRY_BG,
                         fg=styles.FG_COLOR, relief="flat", width=50, height=5, wrap="word")
    desc_entry.pack(pady=(5, 20))

    # ----- Video Path -----
    tk.Label(scroll_frame, text="Video Path:", font=styles.FONT_LABEL,
             fg=styles.FG_COLOR, bg=styles.BG_COLOR).pack()
    video_entry = tk.Entry(scroll_frame, font=styles.FONT_ENTRY, bg=styles.ENTRY_BG,
                           fg=styles.FG_COLOR, insertbackground=styles.FG_COLOR,
                           relief="flat", width=40, justify="center")
    video_entry.pack(pady=(5, 25), ipady=8)

    # ----- Save Button -----
    def save_topic():
        tname = topic_entry.get().strip()
        cname = class_var.get()
        desc = desc_entry.get("1.0", tk.END).strip()
        vpath = video_entry.get().strip()

        if not tname or cname == "Select Class" or not desc or not vpath:
            messagebox.showerror("Error", "All fields must be filled.")
            return

        success = add_new_topic(tname, cname, vpath, desc)
        if success:
            messagebox.showinfo("Success", f"Topic '{tname}' added to '{cname}' successfully.")
            open_edit_topics(root, username, open_admin_dashboard_func)
        else:
            messagebox.showerror("Error", f"Topic '{tname}' already exists in '{cname}'.")

    tk.Button(
        scroll_frame,
        text="Save Topic",
        command=save_topic,
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