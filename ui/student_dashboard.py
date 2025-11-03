# ui/student_dashboard.py
import tkinter as tk
from utils import styles
from db.database import get_classes_by_grade
from ui.login_page import open_login_page


def open_student_dashboard(root, username, grade, open_class_page_func):
    # Clear existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg=styles.BG_COLOR)

    # ----- Top Bar -----
    top_frame = tk.Frame(root, bg=styles.ENTRY_BG, height=70)
    top_frame.pack(fill="x", side="top")

    tk.Label(
        top_frame,
        text=f"Logged in as: {username}",
        font=(styles.FONT_FAMILY, 14),
        fg=styles.FG_COLOR,
        bg=styles.ENTRY_BG
    ).pack(side="left", padx=25, pady=10)

    def logout():
        open_login_page(root, lambda r, u=None, s=None, g=None: None)

    tk.Button(
        top_frame,
        text="Logout",
        command=logout,
        font=(styles.FONT_FAMILY, 12, "bold"),
        bg=styles.BUTTON_PRIMARY,
        fg=styles.BG_COLOR,
        activebackground=styles.BUTTON_PRIMARY,
        activeforeground=styles.BG_COLOR,
        relief="flat",
        width=12,
        height=1,
        cursor="hand2"
    ).pack(side="right", padx=25, pady=10)

    # ----- Main Frame -----
    main_frame = tk.Frame(root, bg=styles.BG_COLOR)
    main_frame.pack(fill="both", expand=True)

    # Title
    tk.Label(
        main_frame,
        text=f"{grade} - Classes",
        font=(styles.FONT_FAMILY, 26, "bold"),
        fg=styles.FG_COLOR,
        bg=styles.BG_COLOR
    ).pack(pady=(30, 20))

    # ----- Scrollable Canvas -----
    canvas = tk.Canvas(main_frame, bg=styles.BG_COLOR, highlightthickness=0)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=styles.BG_COLOR)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Create window to center content horizontally
    canvas_window = canvas.create_window(
        (0, 0),
        window=scroll_frame,
        anchor="n"
    )

    def resize_canvas(event):
        canvas.itemconfig(canvas_window, width=event.width)
    canvas.bind("<Configure>", resize_canvas)

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=100)
    scrollbar.pack(side="right", fill="y")

    # ----- Load Classes -----
    classes = get_classes_by_grade(grade)

    if not classes:
        tk.Label(
            scroll_frame,
            text="No classes assigned for this grade yet.",
            font=(styles.FONT_FAMILY, 14),
            fg=styles.FG_COLOR,
            bg=styles.BG_COLOR
        ).pack(pady=20)
        return

    # ----- Center container for class cards -----
    content_wrapper = tk.Frame(scroll_frame, bg=styles.BG_COLOR)
    content_wrapper.pack(anchor="center")

    for cls in classes:
        class_card = tk.Frame(
            content_wrapper,
            bg=styles.ENTRY_BG,
            relief="flat",
            width=700,
            height=100
        )
        class_card.pack(pady=20)
        class_card.pack_propagate(False)

        tk.Label(
            class_card,
            text=cls,
            font=(styles.FONT_FAMILY, 16, "bold"),
            fg=styles.FG_COLOR,
            bg=styles.ENTRY_BG
        ).pack(pady=(10, 5))

        tk.Button(
            class_card,
            text="View",
            command=lambda c=cls: open_class_page_func(root, username, grade, c),
            font=(styles.FONT_FAMILY, 12, "bold"),
            bg=styles.BUTTON_PRIMARY,
            fg=styles.BG_COLOR,
            relief="flat",
            width=14,
            height=2,
            cursor="hand2"
        ).pack(pady=(0, 10))

    # Enable mouse wheel scroll
    def _on_mousewheel(event):
        canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
