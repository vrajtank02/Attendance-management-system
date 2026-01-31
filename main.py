import os
import operations

def clear_screen():
    """Clears the console screen."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def main():
    """Main function to run the attendance management system."""
    operations.load_data()

    while True:
        clear_screen()
        print("Main Menu:")
        print("1. Add new student")
        print("2. Mark today's attendance")
        print("3. View student's attendance")
        print("4. Exit")
        
        choice = input("Enter your choice (1 - 4): ")

        if choice == "1":
            clear_screen()
            operations.add_new_student()

        elif choice == "2":
            clear_screen()
            operations.mark_attendance_today()

        elif choice == "3":
            clear_screen()
            operations.view_attendance()
        elif choice == "4":
            print("Exiting the program...")
            return
        
        else:
            print("Invalid choice")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()