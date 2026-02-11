import csv
from datetime import datetime
from student import Student

FILE_NAME = "students_records.csv"
students_list = []

def load_data():
    """Loads student data from CSV file into students_list."""
    try:
        with open(FILE_NAME, mode='r') as file:
            reader = csv.reader(file)
            next(reader, None) # Skip header

            for row in reader:
                if not row or len(row) < 5: continue
                
                class_name, r_no, name, date, status = row
                class_name = int(class_name)
                r_no = int(r_no)
                
                student = _find_student(r_no)
                if not student:
                    student = Student(r_no, name, class_name)
                    students_list.append(student)
                
                if date and status:
                    student.mark_attendance(date, status)

    except FileNotFoundError:
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Class", "Roll No", "Name", "Date", "Status"])
        print(f"File '{FILE_NAME}' not found. Created new file with headers.")

def add_new_student():
    """Adds new students to the system."""
    # 1. Get Class
    while True:
        try:
            class_name = int(input("Enter Class (1 -- 12): "))
            if 1 <= class_name <= 12:
                break
            print("Invalid Class. Please enter a number between 1 and 12.")
        except ValueError:
            print("Invalid Class. Please enter a number.")

    # 2. Get Quantity
    try:
        total_student = int(input("How many students do you want to add? "))
    except ValueError:
        print("Invalid number. Adding 1 by default.")
        total_student = 1

    # 3. Add Loop
    for i in range(total_student):
        # Calculate count of students currently in THIS class to generate Roll No
        current_class_count = sum(1 for s in students_list if s.class_name == class_name)
        
        next_number = 101 + current_class_count
        generated_roll_no = int(f"{class_name}{next_number}")

        print(f"\nAdding Student {i+1} | Assigned Roll Number: {generated_roll_no}")
        
        while True:
            name = input(f"Enter the name for {generated_roll_no}:").strip()
            if name and all(x.isalpha() or x.isspace() for x in name):
                break
            print("Invalid name. Please use alphabets only.")

        new_student = Student(generated_roll_no, name, class_name)
        students_list.append(new_student)
        
        _append_to_file(class_name, generated_roll_no, name, "", "")
        print(f"Success! {name} added.")

def mark_attendance_today():
    """Marks attendance for students for today."""
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    day_name = now.strftime("%A")

    if day_name == "Sunday":
        print("Today is Sunday!")
        for s in students_list:
            s.mark_attendance(date, "Holiday")
            _append_to_file(s.class_name, s.roll_number, s.name, date, "Holiday")
        return

    while True:
        try:
            target_class = int(input("Enter Class (1 -- 12): "))
            if 1 <= target_class <= 12: break
            print("Invalid Class.")
        except ValueError:
            print("Invalid input.")

    class_students = [s for s in students_list if s.class_name == target_class]
    
    if not class_students:
        print(f"No students found in Class {target_class}.")
        return

    print(f"\nMarking Attendance for {date} ({day_name})")
    for s in class_students:
        while True:
            status_input = input(f"Roll: {s.roll_number} | {s.name} (P/A): ").lower()
            if status_input in ['p', 'a']:
                status = "Present" if status_input == 'p' else "Absent"
                s.mark_attendance(date, status)
                _append_to_file(s.class_name, s.roll_number, s.name, date, status)
                break
            print("Please enter 'P' for Present or 'A' for Absent.")

def view_attendance():
    """Displays attendance history for a specific student."""
    try:
        roll_no = int(input("Enter Roll Number to view: "))
    except ValueError:
        print("Invalid Roll Number.")
        return

    student = _find_student(roll_no)

    if student:
        print(f"\n--- {student.name} (Class {student.class_name}) ---")
        history = student.get_attendance_history()
        
        if not history:
            print("No attendance records found.")
        else:
            for d, s in history.items():
                print(f"{d}: {s}")
            avg = student.get_average_attendance()
            print(f"Average Attendance: {avg}%")
    else:
        print("Student not found.")

def _find_student(roll_no):
    for s in students_list:
        if s.roll_number == roll_no:
            return s
    return None

def _append_to_file(class_name, r_no, name, date, status):
    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([class_name, r_no, name, date, status])