# ui/topic_page.py
import os
import threading
import tkinter as tk
from tkinter import messagebox
from flask import Flask, send_from_directory, render_template_string
import webview
from utils import styles
from db.database import get_topic_content

# -------------------------------------------------------------------
# Embedded Flask video server (runs once in background)
# -------------------------------------------------------------------
app = Flask(__name__)

VIDEO_DIR = os.path.join(os.getcwd(), "assets", "videos")
current_video = None


@app.route('/')
def index():
    """Render the HTML5 video player page."""
    global current_video
    if not current_video:
        return "<h3>No video selected</h3>"

    video_file, title = current_video
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <style>
            body {{
                background-color: #212121;
                color: #FFFFFF;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: flex-start;
                height: 100vh;
                margin: 0;
            }}
            video {{
                width: 80%;
                max-width: 960px;
                border-radius: 12px;
                box-shadow: 0 0 20px rgba(0,0,0,0.5);
                margin-top: 40px;
            }}
            h2 {{
                font-family: Inter, sans-serif;
                font-size: 24px;
                margin-top: 20px;
                margin-bottom: 10px;
            }}
        </style>
    </head>
    <body>
        <h2>🎬 {title}</h2>
        <video controls autoplay>
            <source src="/video/{video_file}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route('/video/<path:filename>')
def serve_video(filename):
    """Serve the video file to HTML5 player."""
    file_path = os.path.join(VIDEO_DIR, filename)
    if not os.path.exists(file_path):
        return f"<h3>File not found: {file_path}</h3>", 404
    return send_from_directory(VIDEO_DIR, filename)


def start_flask():
    """Start Flask in background thread."""
    app.run(port=5000, debug=False, use_reloader=False)


# -------------------------------------------------------------------
# Topic page for LMS
# -------------------------------------------------------------------
def open_topic_page(root, username, grade, class_name, topic_name,
                    open_class_page_func, open_student_dashboard_func):
    """Displays the topic content player (video + description)."""
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg=styles.BG_COLOR)

    # --- Top Bar ---
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
        command=lambda: open_class_page_func(
            root, username, grade, class_name, open_student_dashboard_func
        ),
        font=(styles.FONT_FAMILY, 12, "bold"),
        bg=styles.BUTTON_PRIMARY,
        fg=styles.BG_COLOR,
        relief="flat",
        width=12,
        height=1,
        cursor="hand2"
    ).pack(side="right", padx=25, pady=10)

    # --- Fetch topic details from DB ---
    video_path, description = get_topic_content(class_name, topic_name)

    if not video_path:
        messagebox.showerror("Video Not Found", f"No video path found for '{topic_name}' in database.")
        return

    # ----------------------------------------------------------------
    # ✅ Cross-Platform Path Normalization (macOS + Windows)
    # ----------------------------------------------------------------
    video_path = video_path.strip().replace("\\", "/")  # normalize slashes
    if video_path.startswith("/"):  # remove accidental leading slash
        video_path = video_path[1:]

    # Convert to absolute path relative to project directory
    abs_video_path = os.path.abspath(os.path.join(os.getcwd(), video_path))

    if not os.path.exists(abs_video_path):
        messagebox.showerror("File Missing", f"Video file not found at:\n{abs_video_path}")
        return

    # --- Ensure Flask server running ---
    if not any(th.name == "FlaskServer" for th in threading.enumerate()):
        t = threading.Thread(target=start_flask, daemon=True, name="FlaskServer")
        t.start()

    # --- Update current video reference ---
    global current_video
    current_video = (os.path.basename(abs_video_path), f"{class_name} - {topic_name}")

    # --- Scrollable section for description ---
    main_frame = tk.Frame(root, bg=styles.BG_COLOR)
    main_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(main_frame, bg=styles.BG_COLOR, highlightthickness=0)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=styles.BG_COLOR)

    scroll_frame.bind("<Configure>",
                      lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="n")
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # --- Title ---
    tk.Label(
        scroll_frame,
        text=f"{class_name} - {topic_name}",
        font=(styles.FONT_FAMILY, 26, "bold"),
        fg=styles.FG_COLOR,
        bg=styles.BG_COLOR
    ).pack(pady=(50, 20))

    # --- Button to open video ---
    def open_video_window():
        webview.create_window(
            f"{class_name} - {topic_name}",
            "http://127.0.0.1:5000/",
            width=1200,
            height=800
        )
        webview.start()

    tk.Button(
        scroll_frame,
        text="▶  Play Video",
        command=open_video_window,
        font=(styles.FONT_FAMILY, 14, "bold"),
        bg=styles.BUTTON_PRIMARY,
        fg=styles.BG_COLOR,
        relief="flat",
        width=20,
        height=2,
        cursor="hand2"
    ).pack(pady=(20, 40))

    # --- Description Card ---
    desc_card = tk.Frame(scroll_frame, bg=styles.ENTRY_BG, relief="flat")
    desc_card.pack(fill="x", padx=100, pady=(10, 50))

    tk.Label(
        desc_card,
        text="Description",
        font=(styles.FONT_FAMILY, 16, "bold"),
        fg=styles.FG_COLOR,
        bg=styles.ENTRY_BG
    ).pack(anchor="w", padx=20, pady=(10, 5))

    tk.Label(
        desc_card,
        text=description if description else "No description provided.",
        wraplength=1000,
        justify="left",
        font=(styles.FONT_FAMILY, 13),
        fg=styles.FG_COLOR,
        bg=styles.ENTRY_BG
    ).pack(anchor="w", padx=20, pady=(0, 20))

    # --- Mouse Scroll ---
    def _on_mousewheel(event):
        canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)