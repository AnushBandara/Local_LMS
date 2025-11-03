# db/database.py
import sqlite3
import os

def init_db():
    db_path = "lms.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # --- USERS TABLE ---
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        password TEXT,
                        status TEXT,
                        grade TEXT
                    )''')

    # --- CLASSES TABLE ---
    cursor.execute('''CREATE TABLE IF NOT EXISTS classes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        class_name TEXT UNIQUE,
                        grade TEXT
                    )''')

    # --- TOPICS TABLE (WITH VIDEO AND DESCRIPTION) ---
    cursor.execute('''CREATE TABLE IF NOT EXISTS topics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        topic_name TEXT,
                        class_name TEXT,
                        video_path TEXT,
                        description TEXT,
                        UNIQUE(topic_name, class_name)
                    )''')

    # --- Insert Default Users ---
    users = [
        ("Anushka", "abc123", "admin", None),
        ("Imashi", "cde456", "student", "Grade 12"),
        ("Chamika", "fgh789", "student", "Grade 13")
    ]
    for user in users:
        cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)", user)

    # --- Insert Default Classes ---
    classes_data = [
        ("Accounting 1", "Grade 12"),
        ("Business Studies 1", "Grade 12"),
        ("Economics 1", "Grade 12"),
        ("Paper Discussions", "Grade 12"),
        ("Accounting 2", "Grade 13"),
        ("Business Studies 2", "Grade 13"),
        ("Economics 2", "Grade 13"),
        ("Paper Discussions", "Grade 13"),
        ("Revision", "Grade 13"),
    ]
    for c in classes_data:
        cursor.execute("INSERT OR IGNORE INTO classes (class_name, grade) VALUES (?, ?)", c)

    # --- Insert Default Topics with video path + description ---
    topics_data = {
        "Accounting 1": 10,
        "Business Studies 1": 6,
        "Economics 1": 7,
        "Accounting 2": 5,
        "Business Studies 2": 6,
        "Economics 2": 7,
        "Paper Discussions": 9,
        "Revision": 4
    }

    default_video = "/assets/videos/Accoounting1Topic1.mp4"
    default_desc = "Sample topic description here."

    for cls, count in topics_data.items():
        for i in range(1, count + 1):
            topic_name = f"Topic {i}"
            video_path = default_video
            description = default_desc

            # Specific topic sample
            if cls == "Accounting 1" and topic_name == "Topic 1":
                video_path = "/assets/videos/Accoounting1Topic1.mp4"
                description = "Introduction to accounting."

            cursor.execute(
                "INSERT OR IGNORE INTO topics (topic_name, class_name, video_path, description) VALUES (?, ?, ?, ?)",
                (topic_name, cls, video_path, description)
            )

    conn.commit()
    conn.close()


def check_login(username, password):
    conn = sqlite3.connect("lms.db")
    cursor = conn.cursor()
    cursor.execute("SELECT status, grade FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result


def get_classes_by_grade(grade):
    conn = sqlite3.connect("lms.db")
    cursor = conn.cursor()
    cursor.execute("SELECT class_name FROM classes WHERE grade=?", (grade,))
    classes = [row[0] for row in cursor.fetchall()]
    conn.close()
    return classes


def get_topics_by_class(class_name):
    conn = sqlite3.connect("lms.db")
    cursor = conn.cursor()
    cursor.execute("SELECT topic_name FROM topics WHERE class_name=?", (class_name,))
    topics = [row[0] for row in cursor.fetchall()]
    conn.close()
    return topics


def get_topic_content(class_name, topic_name):
    conn = sqlite3.connect("lms.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT video_path, description FROM topics WHERE class_name=? AND topic_name=?",
        (class_name, topic_name)
    )
    result = cursor.fetchone()
    conn.close()
    return result if result else (None, None)
