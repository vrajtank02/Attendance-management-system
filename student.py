class Student:
    """Represents a student with roll number, name, class, and attendance records."""
    def __init__(self, roll_number, name, class_name):
        self.roll_number = roll_number
        self.name = name
        self.class_name = class_name  # New Field
        self.__attendance_records = {} 

    def mark_attendance(self, date, status):
        """Marks attendance of a student for a specific date."""
        self.__attendance_records[date] = status

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
