# ui/admin_dashboard.py
import tkinter as tk
from tkinter import ttk
from utils import styles
from ui.edit_users import open_edit_users
from ui.login_page import open_login_page


def open_admin_dashboard(root, username, open_login_page_func):
    """Displays the admin dashboard with 3 main cards."""
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

    # ✅ FIXED LOGOUT BUTTON (simplified call)
    tk.Button(
        top_frame,
        text="Logout",
        command=lambda: open_login_page(root, open_login_page_func),
        font=(styles.FONT_FAMILY, 12, "bold"),
        bg=styles.BUTTON_PRIMARY,
        fg=styles.BG_COLOR,
        relief="flat",
        width=12,
        height=1,
        cursor="hand2"
    ).pack(side="right", padx=25, pady=10)

    # ----- Main Frame -----
    main_frame = tk.Frame(root, bg=styles.BG_COLOR)
    main_frame.pack(fill="both", expand=True)

    # Scrollable canvas
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
        text="Admin Dashboard",
        font=(styles.FONT_FAMILY, 26, "bold"),
        fg=styles.FG_COLOR,
        bg=styles.BG_COLOR
    ).pack(pady=(40, 40))

    # ----- Card generator -----
    def create_card(parent, title, command):
        frame = tk.Frame(parent, bg=styles.ENTRY_BG, relief="flat", width=700, height=140)
        frame.pack(pady=25)
        frame.pack_propagate(False)

        tk.Label(
            frame,
            text=title,
            font=(styles.FONT_FAMILY, 18, "bold"),
            fg=styles.FG_COLOR,
            bg=styles.ENTRY_BG
        ).pack(pady=(15, 10))

        tk.Button(
            frame,
            text="Open",
            command=command,
            font=(styles.FONT_FAMILY, 12, "bold"),
            bg=styles.BUTTON_PRIMARY,
            fg=styles.BG_COLOR,
            relief="flat",
            width=15,
            height=2,
            cursor="hand2"
        ).pack(pady=(0, 15))

    # Cards
    create_card(scroll_frame, "👥 Edit Users", lambda: open_edit_users(root, username, open_admin_dashboard))
    create_card(scroll_frame, "📚 Edit Classes", lambda: open_placeholder_page(root, username, open_admin_dashboard, "Edit Classes"))
    create_card(scroll_frame, "🎬 Edit Topics", lambda: open_placeholder_page(root, username, open_admin_dashboard, "Edit Topics"))

    # Enable mouse scroll
    def _on_mousewheel(event):
        canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)


# -------------------------------------------------------------------
# Placeholder Pages
# -------------------------------------------------------------------
def open_placeholder_page(root, username, open_admin_dashboard_func, page_name):
    """Simple placeholder until actual admin pages are built."""
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg=styles.BG_COLOR)

    # Top Bar
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
        command=lambda: open_admin_dashboard_func(root, username, open_login_page),
        font=(styles.FONT_FAMILY, 12, "bold"),
        bg=styles.BUTTON_PRIMARY,
        fg=styles.BG_COLOR,
        relief="flat",
        width=12,
        height=1,
        cursor="hand2"
    ).pack(side="right", padx=25, pady=10)

    tk.Label(
        root,
        text=f"{page_name} Page",
        font=(styles.FONT_FAMILY, 26, "bold"),
        fg=styles.FG_COLOR,
        bg=styles.BG_COLOR
    ).pack(pady=(200, 20))

    tk.Label(
        root,
        text="(This section is under development)",
        font=(styles.FONT_FAMILY, 14),
        fg=styles.FG_COLOR,
        bg=styles.BG_COLOR
    ).pack()