"""
database.py
-----------
All SQLite work lives here.

When the app starts, this module:
1. Creates students.db if it does not exist
2. Creates the students table if it does not exist
3. Inserts a few sample records the first time (so you can test immediately)
"""

import os
import sqlite3

# Database file sits next to this Python file
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.db")


def get_connection():
    """Open a connection to the SQLite database file."""
    connection = sqlite3.connect(DB_PATH)
    # Return rows as dictionaries: row["name"] instead of row[1]
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the table and add sample students if the table is empty."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            department TEXT NOT NULL,
            semester TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL
        )
        """
    )
    connection.commit()

    cursor.execute("SELECT COUNT(*) AS total FROM students")
    total = cursor.fetchone()["total"]

    # First run only: insert demo data for viva / testing
    if total == 0:
        sample_students = [
            ("CSE001", "Aarav Sharma", 19, "Male", "Computer Science", "3", "9876543210", "aarav.sharma@college.edu"),
            ("CSE002", "Diya Patel", 20, "Female", "Computer Science", "3", "9876501234", "diya.patel@college.edu"),
            ("ECE001", "Rohan Mehta", 21, "Male", "Electronics", "5", "9123456780", "rohan.mehta@college.edu"),
            ("ME001", "Sneha Iyer", 18, "Female", "Mechanical", "1", "9988776655", "sneha.iyer@college.edu"),
            ("CSE003", "Kabir Khan", 22, "Male", "Computer Science", "7", "9012345678", "kabir.khan@college.edu"),
            ("CIV001", "Ananya Reddy", 19, "Female", "Civil", "3", "9090909090", "ananya.reddy@college.edu"),
            ("ECE002", "Vikram Joshi", 20, "Male", "Electronics", "4", "9811112233", "vikram.joshi@college.edu"),
            ("EEE001", "Meera Nair", 21, "Female", "Electrical", "5", "9765432109", "meera.nair@college.edu"),
        ]
        cursor.executemany(
            """
            INSERT INTO students
                (student_id, name, age, gender, department, semester, phone, email)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            sample_students,
        )
        connection.commit()

    connection.close()


def add_student(data):
    """
    Insert one student.
    Returns (True, message) or (False, error message).
    """
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO students
                (student_id, name, age, gender, department, semester, phone, email)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["student_id"].upper(),
                data["name"],
                int(data["age"]),
                data["gender"],
                data["department"],
                data["semester"],
                data["phone"],
                data["email"],
            ),
        )
        connection.commit()
        return True, "Student added successfully."
    except sqlite3.IntegrityError:
        # UNIQUE constraint on student_id failed
        return False, "This Student ID already exists. Please use a unique ID."
    except Exception as error:
        return False, f"Could not add student: {error}"
    finally:
        connection.close()


def get_all_students():
    """Return a list of all students, newest first by row id."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT student_id, name, age, gender, department, semester, phone, email
        FROM students
        ORDER BY id DESC
        """
    )
    rows = [dict(row) for row in cursor.fetchall()]
    connection.close()
    return rows


def search_students(keyword):
    """Search by Student ID or Name (partial match, case-insensitive)."""
    keyword = keyword.strip()
    if not keyword:
        return get_all_students()

    connection = get_connection()
    cursor = connection.cursor()
    like_value = f"%{keyword}%"
    cursor.execute(
        """
        SELECT student_id, name, age, gender, department, semester, phone, email
        FROM students
        WHERE student_id LIKE ? COLLATE NOCASE
           OR name LIKE ? COLLATE NOCASE
        ORDER BY id DESC
        """,
        (like_value, like_value),
    )
    rows = [dict(row) for row in cursor.fetchall()]
    connection.close()
    return rows


def get_student_by_id(student_id):
    """Return one student dictionary, or None if not found."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT student_id, name, age, gender, department, semester, phone, email
        FROM students
        WHERE student_id = ? COLLATE NOCASE
        """,
        (student_id,),
    )
    row = cursor.fetchone()
    connection.close()
    return dict(row) if row else None


def update_student(original_id, data):
    """
    Update an existing student.
    original_id is the Student ID currently stored in the database.
    """
    connection = get_connection()
    cursor = connection.cursor()
    try:
        new_id = data["student_id"].upper()
        # If the ID is changing, make sure the new one is still unique
        if new_id.lower() != original_id.lower():
            cursor.execute(
                "SELECT 1 FROM students WHERE student_id = ? COLLATE NOCASE",
                (new_id,),
            )
            if cursor.fetchone():
                return False, "This Student ID already exists. Please use a unique ID."

        cursor.execute(
            """
            UPDATE students
            SET student_id = ?,
                name = ?,
                age = ?,
                gender = ?,
                department = ?,
                semester = ?,
                phone = ?,
                email = ?
            WHERE student_id = ? COLLATE NOCASE
            """,
            (
                new_id,
                data["name"],
                int(data["age"]),
                data["gender"],
                data["department"],
                data["semester"],
                data["phone"],
                data["email"],
                original_id,
            ),
        )
        if cursor.rowcount == 0:
            return False, "Student not found. It may have been deleted."
        connection.commit()
        return True, "Student details updated successfully."
    except sqlite3.IntegrityError:
        return False, "This Student ID already exists. Please use a unique ID."
    except Exception as error:
        return False, f"Could not update student: {error}"
    finally:
        connection.close()


def delete_student(student_id):
    """Delete one student by Student ID."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "DELETE FROM students WHERE student_id = ? COLLATE NOCASE",
            (student_id,),
        )
        if cursor.rowcount == 0:
            return False, "Student not found."
        connection.commit()
        return True, "Student deleted successfully."
    except Exception as error:
        return False, f"Could not delete student: {error}"
    finally:
        connection.close()


def get_statistics():
    """
    Return:
    - total number of students
    - a list of (department, count) pairs
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM students")
    total = cursor.fetchone()["total"]

    cursor.execute(
        """
        SELECT department, COUNT(*) AS count
        FROM students
        GROUP BY department
        ORDER BY department
        """
    )
    by_department = [(row["department"], row["count"]) for row in cursor.fetchall()]
    connection.close()
    return total, by_department
