# Attendance Management System

A command-line application built with Python to manage student attendance records. It supports adding students, marking daily attendance, and viewing attendance history with average attendance percentages.

## Features

- **Add New Students** — Register students by class (1–12) with auto-generated roll numbers.
- **Mark Attendance** — Record daily attendance (Present/Absent) per class; Sundays are automatically marked as holidays.
- **View Attendance** — Look up a student's attendance history and average attendance percentage.
- **Persistent Storage** — All records are saved to a CSV file (`students_records.csv`).

## Project Structure

| File | Description |
|---|---|
| `main.py` | Entry point with the main menu loop |
| `student.py` | `Student` class with attendance tracking and average calculation |
| `operations.py` | Core logic — loading data, adding students, marking & viewing attendance |
| `students_records.csv` | CSV file storing all student and attendance data |

## Requirements

- Python 3.x

No external dependencies are required.

## How to Run

```bash
python main.py
```

## Usage

On launch you are presented with a menu:

```
Main Menu:
1. Add new student
2. Mark today's attendance
3. View student's attendance
4. Exit
```

1. **Add new student** — Enter a class number and student name. A roll number is generated automatically (e.g., `12101` for the first student in class 12).
2. **Mark today's attendance** — Select a class and mark each student as Present (`P`) or Absent (`A`).
3. **View student's attendance** — Enter a class and roll number to see the full attendance history and overall percentage.
4. **Exit** — Quit the application.

## CSV Format

| Class | Roll No | Name | Date | Status |
|---|---|---|---|---|
| 12 | 12101 | Vraj Tank | 31/01/2026 | Present |

## License

This project is for educational purposes.
