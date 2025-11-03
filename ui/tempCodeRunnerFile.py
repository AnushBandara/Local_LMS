# ui/login_page.py
import tkinter as tk
from tkinter import messagebox
from db.database import check_login
from utils import styles

def open_login_page(root, open_next_page):
    # Clear previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg=styles.BG_COLOR)

    # Outer full-screen frame
    outer_frame = tk.Frame(root, bg=styles.BG_COLOR)
    outer_frame.pack(fill="both", expand=True)

    # Centered card
    card = tk.Frame(outer_frame, bg=styles.ENTRY_BG, bd=0, relief="flat")
    card.place(relx=0.5, rely=0.5, relwidth=0.35, relheight=0.55, anchor="center")

    # Title
    tk.Label(
        card,
        text="Login",
        font=styles.FONT_TITLE,
        fg=styles.FG_COLOR,
        bg=styles.ENTRY_BG
    ).pack(pady=(40, 25))

    # Username label + entry
    tk.Label(card, text="Username:", font=styles.FONT_LABEL, fg=styles.FG_COLOR, bg=styles.ENTRY_BG).pack()
    username_entry = tk.Entry(
        card,
        width=28,
        font=styles.FONT_ENTRY,
        bg=styles.BG_COLOR,
        fg=styles.FG_COLOR,
        insertbackground=styles.FG_COLOR,
        relief="flat",
        justify="center"
    )
    username_entry.pack(pady=(5, 15), ipady=10)

    # Password label + entry
    tk.Label(card, text="Password:", font=styles.FONT_LABEL, fg=styles.FG_COLOR, bg=styles.ENTRY_BG).pack()
    password_entry = tk.Entry(
        card,
        width=28,
        font=styles.FONT_ENTRY,
        bg=styles.BG_COLOR,
        fg=styles.FG_COLOR,
        insertbackground=styles.FG_COLOR,
        relief="flat",
        show="*",
        justify="center"
    )
    password_entry.pack(pady=(5, 10), ipady=10)

    # --- Show Password toggle ---
    def toggle_password():
        if password_entry.cget("show") == "":
            password_entry.config(show="*")
            show_pass_btn.config(text="Show Password")
        else:
            password_entry.config(show="")
            show_pass_btn.config(text="Hide Password")

    show_pass_btn = tk.Checkbutton(
        card,
        text="Show Password",
        font=(styles.FONT_FAMILY, 10),
        bg=styles.ENTRY_BG,
        fg=styles.FG_COLOR,
        selectcolor=styles.ENTRY_BG,
        activebackground=styles.ENTRY_BG,
        command=toggle_password
    )
    show_pass_btn.pack(pady=(0, 25))

    # --- Login function ---
    def login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        status = check_login(username, password)
        if status:
            messagebox.showinfo("Success", f"Welcome {username}! You are logged in as {status}.")
            outer_frame.destroy()
            open_next_page(root)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    # --- Login button ---
    login_button = tk.Button(
        card,
        text="Login",
        command=login,
        font=styles.FONT_BUTTON,
        bg=styles.BUTTON_PRIMARY,
        fg=styles.BG_COLOR,
        activebackground=styles.BUTTON_PRIMARY,
        activeforeground=styles.BG_COLOR,
        relief="flat",
        width=20,
        height=2,
        cursor="hand2"
    )
    login_button.pack(pady=(5, 20))
