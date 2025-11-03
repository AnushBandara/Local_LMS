# ui/class_page.py
import tkinter as tk
from utils import styles
from db.database import get_topics_by_class
from ui.topic_page import open_topic_page

def open_class_page(root, username, grade, class_name, open_student_dashboard_func):
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

    tk.Button(
        top_frame,
        text="Back",
        command=lambda: open_student_dashboard_func(
            root, username, grade,
            lambda r, u, g, c: open_class_page(r, u, g, c, open_student_dashboard_func)
        ),
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

    # ----- Class Title -----
    tk.Label(
        root,
        text=class_name,
        font=(styles.FONT_FAMILY, 28, "bold"),
        fg=styles.FG_COLOR,
        bg=styles.BG_COLOR
    ).pack(pady=(80, 30))

    # ----- Scrollable Section -----
    main_frame = tk.Frame(root, bg=styles.BG_COLOR)
    main_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(main_frame, bg=styles.BG_COLOR, highlightthickness=0)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=styles.BG_COLOR)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="n")
    def resize_canvas(event):
        canvas.itemconfig(canvas_window, width=event.width)
    canvas.bind("<Configure>", resize_canvas)

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=100)
    scrollbar.pack(side="right", fill="y")

    # ----- Load Topics -----
    topics = get_topics_by_class(class_name)

    if not topics:
        tk.Label(
            scroll_frame,
            text="No topics available for this class yet.",
            font=(styles.FONT_FAMILY, 14),
            fg=styles.FG_COLOR,
            bg=styles.BG_COLOR
        ).pack(pady=20)
        return

    # Center content
    content_wrapper = tk.Frame(scroll_frame, bg=styles.BG_COLOR)
    content_wrapper.pack(anchor="center")

    for topic in topics:
        topic_card = tk.Frame(
            content_wrapper,
            bg=styles.ENTRY_BG,
            relief="flat",
            width=700,
            height=80
        )
        topic_card.pack(pady=15)
        topic_card.pack_propagate(False)

        tk.Label(
            topic_card,
            text=topic,
            font=(styles.FONT_FAMILY, 16, "bold"),
            fg=styles.FG_COLOR,
            bg=styles.ENTRY_BG
        ).pack(pady=(10, 5))

        tk.Button(
            topic_card,
            text="View",
            command=lambda t=topic: open_topic_page(root, username, grade, class_name, t, open_class_page, open_student_dashboard_func),
            font=(styles.FONT_FAMILY, 12, "bold"),
            bg=styles.BUTTON_PRIMARY,
            fg=styles.BG_COLOR,
            relief="flat",
            width=14,
            height=2,
            cursor="hand2"
        ).pack(pady=(0, 10))

    # Enable mouse wheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
