class Student:
    """Represents a student with roll number, name, class, and attendance records."""
    
    VALID_STATUSES = ["Present", "Absent", "Holiday"]

    def __init__(self, roll_number, name, class_name):
        if not isinstance(roll_number, int):
            raise ValueError("Roll number must be an integer.")
        if roll_number <= 0:
            raise ValueError("Roll number must be greater than 0.")
        
        if not isinstance(name, str):
            raise ValueError("Name must be in string.")
        if not name.strip():
            raise ValueError("Name cannot be blank or contain only spaces.")
        
        if not isinstance(class_name, int):
            raise ValueError("Class must be an integer.")
        if not (1 <= class_name <= 12):
            raise ValueError("Class must be between 1 and 12.")
        
        self.roll_number = roll_number
        self.name = name.strip()
        self.class_name = class_name
        self.__attendance_records = {} 

    def mark_attendance(self, date, status):
        """Marks attendance of a student for a specific date."""
        if not isinstance(date, str):
            raise ValueError(f"Date must be a string, but got {type(date).__name__}.")
        if not date.strip():
            raise ValueError("Date cannot be blank.")
            
        if not isinstance(status, str):
            raise ValueError("Status must be a string.")
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: '{status}'. Must be one of {self.VALID_STATUSES}.")
            
        self.__attendance_records[date.strip()] = status

    def get_attendance_history(self):
        """Returns the attendance records of the student."""
        return self.__attendance_records

    def get_average_attendance(self):
        """Calculates and returns the average attendance percentage of the student."""
        total_days = len(self.__attendance_records)
        if total_days == 0:
            return 0.0
        present_count = list(self.__attendance_records.values()).count('Present')
        return round((present_count / total_days) * 100, 2)