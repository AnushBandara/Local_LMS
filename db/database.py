# db/database.py
import sqlite3
import os

def init_db():
    db_path = "lms.db"
    new_db = not os.path.exists(db_path)  # ✅ Detect first-time creation

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # --- Create tables if not exist ---
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        password TEXT,
                        status TEXT,
                        grade TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS classes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        class_name TEXT UNIQUE,
                        grade TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS topics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        topic_name TEXT,
                        class_name TEXT,
                        video_path TEXT,
                        description TEXT,
                        UNIQUE(topic_name, class_name)
                    )''')

    # ✅ Insert default data only if database is new
    if new_db:
        # --- Default Users ---
        users = [
            ("Anushka", "abc123", "admin", None),
            ("Imashi", "cde456", "student", "Grade 12"),
            ("Chamika", "fgh789", "student", "Grade 13")
        ]
        for user in users:
            cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", user)

        # --- Default Classes ---
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
            cursor.execute("INSERT INTO classes (class_name, grade) VALUES (?, ?)", c)

        # --- Default Topics ---
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
                if cls == "Accounting 1" and topic_name == "Topic 1":
                    video_path = "/assets/videos/Accoounting1Topic1.mp4"
                    description = "Introduction to accounting."
                cursor.execute(
                    "INSERT INTO topics (topic_name, class_name, video_path, description) VALUES (?, ?, ?, ?)",
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


def get_all_users():
    """Return list of all users as (username, status, grade)."""
    conn = sqlite3.connect("lms.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, status, grade FROM users ORDER BY status DESC")
    users = cursor.fetchall()
    conn.close()
    return users


def delete_user(username):
    """Delete a user from the database."""
    conn = sqlite3.connect("lms.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    conn.close()


def add_new_user(username, password, status, grade):
    """Insert a new user. Returns True if successful, False if username exists."""
    conn = sqlite3.connect("lms.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (username, password, status, grade))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_all_classes():
    """Return list of all classes as (class_name, grade)."""
    conn = sqlite3.connect("lms.db")
    cursor = conn.cursor()
    cursor.execute("SELECT class_name, grade FROM classes ORDER BY grade ASC")
    classes = cursor.fetchall()
    conn.close()
    return classes


def delete_class(class_name):
    """Delete a class from the database."""
    conn = sqlite3.connect("lms.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM classes WHERE class_name=?", (class_name,))
    conn.commit()
    conn.close()

def add_new_class(class_name, grade):
    """Insert a new class. Returns True if successful, False if class already exists."""
    conn = sqlite3.connect("lms.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO classes (class_name, grade) VALUES (?, ?)", (class_name, grade))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_topics():
    """Return all topics with their associated class names (no duplicates removed)."""
    conn = sqlite3.connect("lms.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT topic_name, class_name
        FROM topics
        ORDER BY class_name ASC, topic_name ASC
    """)
    topics = cursor.fetchall()
    conn.close()
    return topics



def get_all_class_names():
    """Return list of all existing class names."""
    conn = sqlite3.connect("lms.db")
    cursor = conn.cursor()
    cursor.execute("SELECT class_name FROM classes ORDER BY class_name ASC")
    classes = [row[0] for row in cursor.fetchall()]
    conn.close()
    return classes


def add_new_topic(topic_name, class_name, video_path, description):
    """Insert a new topic for a given class with video path and description."""
    conn = sqlite3.connect("lms.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO topics (topic_name, class_name, video_path, description) VALUES (?, ?, ?, ?)",
            (topic_name, class_name, video_path, description)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def delete_topic(topic_name, class_name):
    """Delete a specific topic belonging to a class."""
    conn = sqlite3.connect("lms.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM topics WHERE topic_name=? AND class_name=?", (topic_name, class_name))
    conn.commit()
    conn.close()