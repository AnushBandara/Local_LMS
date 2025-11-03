# embedded_video_one_window.py
import os
import threading
import tkinter as tk
from flask import Flask, send_from_directory, render_template_string
import webview

# -------------------------------
# Flask setup (serve local video)
# -------------------------------
app = Flask(__name__)
VIDEO_DIR = os.path.join(os.getcwd(), "assets/videos")
VIDEO_FILE = "Accounting1Topic1.mp4"
PORT = 5050

@app.route("/")
def index():
    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                background-color: #212121;
                color: #FFFFFF;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100%;
                margin: 0;
            }}
            video {{
                width: 80%;
                max-width: 960px;
                border-radius: 12px;
                box-shadow: 0 0 15px rgba(0,0,0,0.5);
            }}
            h2 {{
                color: #FFFFFF;
                font-family: Inter, sans-serif;
            }}
        </style>
    </head>
    <body>
        <h2>🎬 Embedded LMS Video Player</h2>
        <video controls autoplay>
            <source src="http://127.0.0.1:{PORT}/video/{VIDEO_FILE}" type="video/mp4">
        </video>
    </body>
    </html>
    """)

@app.route("/video/<path:filename>")
def video(filename):
    return send_from_directory(VIDEO_DIR, filename)

def start_flask():
    app.run(port=PORT, debug=False, use_reloader=False)


# -------------------------------
# Tkinter + Embedded Webview
# -------------------------------
def start_gui():
    root = tk.Tk()
    root.title("Chamika LMS - Embedded Video Player")
    root.geometry("1280x800")
    root.configure(bg="#212121")

    # --- Header bar ---
    header = tk.Frame(root, bg="#424242", height=70)
    header.pack(fill="x", side="top")
    tk.Label(
        header,
        text="Chamika LMS | Embedded Video Player",
        font=("Inter", 18, "bold"),
        fg="#FFFFFF",
        bg="#424242"
    ).pack(side="left", padx=20)

    # --- Video frame (where the webview will be embedded) ---
    video_frame = tk.Frame(root, bg="#212121")
    video_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # --- Start Flask server in background ---
    threading.Thread(target=start_flask, daemon=True).start()

    # --- Create the webview window and embed inside Tkinter frame ---
    window = webview.create_window(
        "Video Player",
        url=f"http://127.0.0.1:{PORT}/",
        width=1200,
        height=700,
        resizable=True,
        background_color="#212121"
    )

    # Embed webview inside Tkinter window handle (no new window)
    window.gui = 'tkinter'
    window.master = video_frame  # attach to this frame
    webview.start(gui='tkinter', debug=False)

if __name__ == "__main__":
    start_gui()