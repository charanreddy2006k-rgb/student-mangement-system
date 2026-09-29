"""
student.py
----------
Holds simple helper functions for a Student record.

This file is kept small on purpose so a beginner can see:
- how data is grouped into a dictionary
- how we check (validate) user input before saving
"""

import re


# Fields that must not be empty when adding a student
REQUIRED_FIELDS = (
    "student_id",
    "name",
    "age",
    "gender",
    "department",
    "semester",
    "phone",
    "email",
)


def empty_student():
    """Return a dictionary with all student fields set to empty strings."""
    return {
        "student_id": "",
        "name": "",
        "age": "",
        "gender": "",
        "department": "",
        "semester": "",
        "phone": "",
        "email": "",
    }


def clean_text(value):
    """Remove extra spaces from the start and end of a string."""
    if value is None:
        return ""
    return str(value).strip()


def validate_student(data, is_update=False):
    """
    Check that student details are complete and look correct.

    data       -> dictionary with the form values
    is_update  -> True when we are editing an existing student
                  (Student ID is still required, uniqueness is checked in database.py)

    Returns (True, "") if everything is OK.
    Returns (False, "error message") if something is wrong.
    """
    cleaned = {}
    for field in REQUIRED_FIELDS:
        cleaned[field] = clean_text(data.get(field, ""))

    # 1) Required fields
    missing = []
    for field in REQUIRED_FIELDS:
        if not cleaned[field]:
            # Show a nicer name in the error (student_id -> Student ID)
            nice_name = field.replace("_", " ").title()
            missing.append(nice_name)

    if missing:
        return False, "Please fill all required fields:\n" + ", ".join(missing)

    # 2) Student ID: letters, digits, hyphen only (easy college IDs like CSE001)
    student_id = cleaned["student_id"]
    if len(student_id) < 2 or len(student_id) > 20:
        return False, "Student ID must be between 2 and 20 characters."
    if not re.fullmatch(r"[A-Za-z0-9\-]+", student_id):
        return False, "Student ID can only contain letters, numbers, and hyphens."

    # 3) Name
    name = cleaned["name"]
    if len(name) < 2:
        return False, "Name must have at least 2 characters."
    if not re.fullmatch(r"[A-Za-z .']+", name):
        return False, "Name should contain only letters, spaces, dots, or apostrophes."

    # 4) Age: whole number between 15 and 80 (typical college range)
    try:
        age = int(cleaned["age"])
    except ValueError:
        return False, "Age must be a whole number."
    if age < 15 or age > 80:
        return False, "Age must be between 15 and 80."
    cleaned["age"] = str(age)

    # 5) Gender
    gender = cleaned["gender"]
    allowed_genders = ("Male", "Female", "Other")
    if gender not in allowed_genders:
        return False, "Please select a valid gender (Male, Female, or Other)."

    # 6) Department and semester
    if len(cleaned["department"]) < 2:
        return False, "Please enter a valid department."
    if len(cleaned["semester"]) < 1:
        return False, "Please select a semester."

    # 7) Phone: digits only, 10 digits (common Indian mobile length)
    phone = cleaned["phone"]
    # Allow spaces or dashes in typing, then keep digits only
    phone_digits = re.sub(r"\D", "", phone)
    if not phone_digits.isdigit():
        return False, "Phone number should contain valid digits only."
    if len(phone_digits) != 10:
        return False, "Phone number must have exactly 10 digits."
    cleaned["phone"] = phone_digits

    # 8) Email: basic check (something@something.something)
    email = cleaned["email"].lower()
    if not re.fullmatch(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", email):
        return False, "Please enter a valid email address (example: name@college.edu)."
    cleaned["email"] = email

    return True, cleaned
