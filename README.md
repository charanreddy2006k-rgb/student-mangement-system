# Student Management System

A beginner-friendly **Python mini project** for managing student records.

This application is suitable for a **3rd-semester engineering mini project and viva**. It uses only:

- **Python 3**
- **SQLite** (comes with Python)
- **Tkinter** (comes with Python on most Windows installs)

No extra libraries and no internet connection are required.

---

## Features

1. **Add Student** – ID, name, age, gender, department, semester, phone, email  
2. **View Students** – all records in a table  
3. **Search Student** – by Student ID or name  
4. **Update Student** – edit a selected record  
5. **Delete Student** – delete after confirmation  
6. **Statistics** – total students and department-wise count  
7. **Permanent storage** – SQLite database (`students.db`) created automatically  

Validation included:

- Student ID must be unique  
- Required fields cannot be empty  
- Phone number must be 10 digits  
- Email must look like `name@domain.com`  
- Clear error and success messages  

---

## Project structure

```
student-management-system/
├── main.py          # GUI (Tkinter window, forms, table, menus)
├── database.py      # SQLite create / insert / search / update / delete
├── student.py       # Input validation helpers
├── students.db      # Created automatically on first run
└── README.md        # This file
```

How the files connect:

- `main.py` starts the window and calls functions from `database.py` and `student.py`
- `database.py` talks to SQLite only
- `student.py` checks the form data before saving

---

## How to install and run

### 1. Install Python

Install **Python 3.10 or later** from [https://www.python.org/downloads/](https://www.python.org/downloads/).

On Windows, tick **Add Python to PATH** during setup.

Check the install in Command Prompt or PowerShell:

```bash
python --version
```

If that fails, try:

```bash
py --version
```

### 2. Open the project folder

```bash
cd C:\Users\ASUS\student-management-system
```

### 3. Run the application

```bash
python main.py
```

or:

```bash
py main.py
```

A window titled **Student Management System** should open.

**First run:** the program creates `students.db` and inserts **8 sample students** so you can test View, Search, Update, and Delete immediately.

---

## How to use (for demo / viva)

1. **Dashboard** – total students and shortcuts  
2. **All Students** – table of records; type a name or ID and click **Search**  
3. Select a row, then **Update Selected** or **Delete Selected**  
4. **Add Student** – fill the form and click **Save Student**  
5. **Statistics** – total count and department-wise table  

Double-click a table row to open the update form.

---

## Sample records (loaded on first run)

| Student ID | Name          | Department         | Semester |
|-----------|---------------|--------------------|----------|
| CSE001    | Aarav Sharma  | Computer Science   | 3        |
| CSE002    | Diya Patel    | Computer Science   | 3        |
| ECE001    | Rohan Mehta   | Electronics        | 5        |
| ME001     | Sneha Iyer    | Mechanical         | 1        |
| CSE003    | Kabir Khan    | Computer Science   | 7        |
| CIV001    | Ananya Reddy  | Civil              | 3        |
| ECE002    | Vikram Joshi  | Electronics        | 4        |
| EEE001    | Meera Nair    | Electrical         | 5        |

To start with an empty database, close the app and delete `students.db`, then run `python main.py` again. Sample data will be inserted again if the table is empty.

---

## Requirements

| Item        | Needed?                          |
|-------------|----------------------------------|
| Python 3    | Yes                              |
| pip packages| **None**                         |
| SQLite      | Built into Python                |
| Tkinter     | Built into standard Python on Windows |

If Tkinter is missing (rare on Windows), install Python again and enable **tcl/tk**.

---

## Possible viva questions

- **Why SQLite?** It is a file-based database, needs no server, and is included with Python.  
- **Where is data stored?** In `students.db` in the project folder.  
- **How is Student ID unique?** The `student_id` column has a `UNIQUE` constraint.  
- **What happens if validation fails?** The record is not saved; an error message is shown.  
- **MVC-style split?** GUI (`main.py`), data (`database.py`), rules (`student.py`).  

---

## License

Created as an academic mini project. You may copy and modify it for college submissions.
