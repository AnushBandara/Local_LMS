# main.py
import tkinter as tk
from db.database import init_db
from ui.login_page import open_login_page
from ui.student_dashboard import open_student_dashboard
from ui.class_page import open_class_page
from ui.admin_dashboard import open_admin_dashboard  # ✅ added
from utils import styles


def next_page(root, username, status, grade):
    # Student flow
    if status == "student":
        open_student_dashboard(
            root,
            username,
            grade,
            lambda r, u, g, c: open_class_page(r, u, g, c, open_student_dashboard)
        )
    # Admin flow
    elif status == "admin":
        open_admin_dashboard(root, username, open_login_page)
    else:
        frame = tk.Frame(root, bg=styles.BG_COLOR)
        frame.pack(fill="both", expand=True)
        tk.Label(frame, text="Invalid user role.",
                 font=styles.FONT_TITLE, fg=styles.FG_COLOR, bg=styles.BG_COLOR).pack(expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Learning Management System")

    try:
        root.state("zoomed")  # Full screen (Windows)
    except:
        root.attributes("-zoomed", True)  # macOS/Linux fallback

    root.configure(bg=styles.BG_COLOR)

    init_db()
    open_login_page(root, next_page)
    root.mainloop()