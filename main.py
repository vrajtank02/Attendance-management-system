
"""3 windows created successfully!
Review the code before run this program.
in the main window it will ask to the user press 1 to Mark attendance press 2 to Review  attendance Press 3 to close the  program."""
# if you want go back to main window enter'close' Instead of serial number in both windows.

import csv
from datetime import datetime

now=datetime.now()

FILE_NAME = "attendance.csv"

def main():
    while True:
        user_input=input("enter 1 for mark attendance enter 2 for Review attendance enter 3 for close attendance.")

        if user_input=="1":
            while True:
                s_no=input('enter your role number')
#close the mark attendance window by 'close' Instead of serial number
                if s_no.lower() == 'close':
                    break

                name=input('enter your name')

                date=now.strftime("%d/%m/%y") 

                status=input('enter P for present or enter A for apsent').lower()

                if status=='a':
                    status='apsent'
                else:
                    status='present'

                with open(FILE_NAME, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([ s_no, name, date, status])
                print(f"Attendance saved for {name}!")

# Review attendance
        if user_input=='2':
            while True:
                search_sno = input("Enter Serial Number to search: ")
#close the Review attendance window   by enter 'close' Instead of serial number
                if search_sno.lower() =='close':
                    break

                with open(FILE_NAME, mode='r') as file:
                    reader=csv.reader(file)
                    for row in reader:
                        if row[0] == search_sno:
                            print(f"s.no:{row[0]}")
                            print(f"Name: {row[1]}")
                            print(f"Date: {row[2]}")
                            print(f"Status: {row[3]}")

#close the Program
        if user_input=='3':
            break

if __name__=='__main__':   #run the main window
    main()