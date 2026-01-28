import csv
from datetime import datetime
from student import Student

FILE_NAME = "students_records.csv"
students_list = []

def load_data():
    """Loads student data from CSV file into students_list."""
    with open(FILE_NAME, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if not row: continue
            class_name, r_no, name, date, status = row
            
            class_name = int(class_name)
            r_no = int(r_no)
            
            student = _find_student(r_no)
            
            if not student:
                student = Student(r_no, name, class_name)
                students_list.append(student)
            
            if date and status:
                student.mark_attendance(date, status)

def add_new_student():
    """Adds a new student to the system."""
    class_name = int(input("Enter Class (1 -- 12): "))

    count = 0
    for s in students_list:
        if s.class_name == class_name:
            count += 1
    
    next_number = 101 + count
    generated_roll_no = int(str(class_name) + str(next_number))
    
    print(f"Assigning Roll Number: {generated_roll_no}")
    
    name = input("Enter Student Name: ")
    
    new_student = Student(generated_roll_no, name, class_name)
    students_list.append(new_student)
    
    _append_to_file(class_name, generated_roll_no, name, "", "")
    
    print(f"Success! {name} (Roll: {generated_roll_no}) added to Class {class_name}.")

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
            
        print("Holiday marked for everyone.")
        return

    target_class = int(input("Enter Class to mark attendance: "))

    class_students = []
    for s in students_list:
        if s.class_name == target_class:
            class_students.append(s)
    
    if not class_students:
        print(f"No students found in Class {target_class}.")
        return

    print(f"Marking Attendance for {date} ({day_name}) ")
    for s in class_students:
        print(f"Roll: {s.roll_number} | Name: {s.name}")
        status_input = input("Status (P/A): ").lower()
        
        if status_input == 'a':
            status = "Absent"
        elif status_input == 'p':
            status = "Present"
        
        s.mark_attendance(date, status)
        _append_to_file(s.class_name, s.roll_number, s.name, date, status)

    print("Attendance marked successfully!")

def view_attendance():
    """Displays attendance history and average attendance for a specific student."""
    target_class = int(input("Enter Class: "))
    
    roll_no = int(input("Enter Roll Number: "))

    student = _find_student(roll_no)

    if student and student.class_name == target_class:
        print("--- Student Details: ---")
        print(f"Roll No: {student.roll_number} | Name: {student.name}")
        print("Date: | Status")
        
        history = student.get_attendance_history()
        
        for date, status in history.items():
            print(f"{date:} | {status}")

        avg = student.get_average_attendance()
        print(f"Average Attendance: {avg}%")
        
    else:
        print("Student not found in this Class.")

def _find_student(roll_no):
    """Finds and returns a student by roll number."""
    for s in students_list:
        if s.roll_number == roll_no:
            return s
    return None

def _append_to_file(class_name, r_no, name, date, status):
    """Appends a new record to the CSV file.
    ispecially used when adding new students or marking attendance.
    """
    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([class_name, r_no, name, date, status])