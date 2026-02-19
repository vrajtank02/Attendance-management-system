import csv
from datetime import datetime
from student import Student

FILE_NAME = "students_records.csv"
students_list = []

def load_data():
    """Loads student data from CSV file into students_list."""
    print("Loading student data from the file, Please wait...")
    try:
        with open(FILE_NAME, mode='r') as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                if not row: continue
                
                if len(row) != 5:
                    print(f"Warning: Skipping malformed row: {row}")
                    continue
                
                class_name_str, r_no_str, name, date, status = row
                
                try:
                    class_name = int(class_name_str)
                    r_no = int(r_no_str)
                    
                    student = _find_student(r_no)
                    
                    if not student:
                        student = Student(r_no, name, class_name)
                        students_list.append(student)
                    
                    if date and status:
                        student.mark_attendance(date, status)
                        
                except ValueError as e:
                    print(f"Warning: Skipping invalid data in row {row}. Reason: {e}")
                    continue
        print("Data loaded successfully!")
    except FileNotFoundError:
        _save_all_data()
        print(f"File '{FILE_NAME}' not found. Created new file.")
    except PermissionError:
        print(f"CRITICAL ERROR: '{FILE_NAME}' is currently open in another program.")
        print("Please close it and restart the program.")
        exit()
    input("\nPress enter to continue...")

def add_new_student():
    """Adds new students to the system."""
    while True:
        try:
            class_name = int(input("Enter Class (1 - 12): "))
            if 1 <= class_name <= 12:
                break
            else:
                print("Invalid Class. Please enter a number between 1 and 12.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    while True:
        try:
            total_student = int(input("How many students do you want to add? "))
            if total_student > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    for i in range(total_student):
        count = sum(1 for s in students_list if s.class_name == class_name)
        next_number = 101 + count
        generated_roll_no = int(str(class_name) + str(next_number))
        
        print(f"\nAdding Student {i+1} | Assigning Roll Number: {generated_roll_no}")
        
        while True:
            name = input("Enter Student Name: ").strip()
            if name and all(x.isalpha() or x.isspace() for x in name):
                break
            else:
                print("Invalid name. Please use alphabets and spaces only.")
        
        try:
            new_student = Student(generated_roll_no, name, class_name)
            students_list.append(new_student)
            print(f"Success! {name} (Roll: {generated_roll_no}) added to Class {class_name}.")
        except ValueError as e:
            print(f"Failed to add student due to validation error: {e}")

    _save_all_data()

def mark_attendance_today():
    """Marks attendance for students for today."""
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    day_name = now.strftime("%A")

    if day_name == "Sunday":
        print("Today is Sunday!")
        for s in students_list:
            if date not in s.get_attendance_history():
                s.mark_attendance(date, "Holiday")
        _save_all_data()
        print("Holiday marked for everyone.")
        return

    while True:
        try:
            target_class = int(input("Enter Class to mark attendance (1 - 12): "))
            if 1 <= target_class <= 12:
                break
            print("Invalid Class. Please enter a number between 1 and 12.")
        except ValueError:
            print("Invalid input. Class must be a number.")

    class_students = [s for s in students_list if s.class_name == target_class]
    
    if not class_students:
        print(f"No students found in Class {target_class}.")
        return

    students_to_mark = [s for s in class_students if date not in s.get_attendance_history()]

    if not students_to_mark:
        print(f"Attendance for {date} is already fully marked for Class {target_class}.")
        return

    print(f"Marking Attendance for {date} ({day_name})")
    for s in students_to_mark:
        print(f"Roll: {s.roll_number} | Name: {s.name}")
        while True:
            status_input = input("Status (Enter P to mark present, A to mark absent): ").strip().upper()
            if status_input == 'P':
                status = "Present"
                break
            elif status_input == 'A':
                status = "Absent"
                break
            else:
                print("Invalid input. Please enter 'P' or 'A' only.")
        
        try:
            s.mark_attendance(date, status)
        except ValueError as e:
            print(f"Error marking attendance: {e}")

    _save_all_data()
    print("Attendance saved successfully!")

def view_attendance():
    """Displays attendance history and average attendance for a specific student."""
    while True:
        try:
            target_class = int(input("Enter Class (1 - 12): "))
            if 1 <= target_class <= 12:
                break
            print("Invalid Class. Please enter a number between 1 and 12.")
        except ValueError:
            print("Invalid input. Class must be a number.")

    while True:
        try:
            roll_no = int(input("Enter Roll Number: "))
            break
        except ValueError:
            print("Invalid input. Roll Number must be a number.")

    student = _find_student(roll_no)

    if student and student.class_name == target_class:
        print("\n--- Student Details ---")
        print(f"Roll No: {student.roll_number} | Name: {student.name}")
        print("Date       | Status")
        print("-" * 25)
        
        history = student.get_attendance_history()
        if not history:
            print("No attendance records found.")
        else:
            for d, status in history.items():
                print(f"{d} | {status}")

        avg = student.get_average_attendance()
        print("-" * 25)
        print(f"Average Attendance: {avg}%")
        
    else:
        print("Student not found in this Class.")

def _find_student(roll_no):
    """Finds and returns a student by roll number."""
    for s in students_list:
        if s.roll_number == roll_no:
            return s
    return None

def _save_all_data():
    """Overwrites the CSV file with the current data in memory.
    This prevents duplicate records and keeps the single-file structure clean.
    """
    try:
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Class", "Roll No", "Name", "Date", "Status"])
            
            for s in students_list:
                history = s.get_attendance_history()
                if not history:
                    writer.writerow([s.class_name, s.roll_number, s.name, "", ""])
                else:
                    for d, status in history.items():
                        writer.writerow([s.class_name, s.roll_number, s.name, d, status])
                        
    except PermissionError:
        print(f"Error: Permission denied. Please ensure '{FILE_NAME}' is closed before proceeding.")
    except IOError as e:
        print(f"Error: Could not write to file '{FILE_NAME}': {e}")