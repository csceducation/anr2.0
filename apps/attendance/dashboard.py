import pymongo
from apps.staffs.models import Staff
from apps.students.models import Student

class DashboardManager:
    def __init__(self, mongodb_database):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client[mongodb_database]
        self.staff_collection = self.db["staff_collection"]
        self.student_collection = self.db["student_collection"]

    def __del__(self):
        self.client.close()

    def get_staff_attendance(self, week_dates):
        staff_strength = Staff.objects.count()
        presentees = []

        for date in week_dates:
            staff_attendance = self.staff_collection.find_one({'date': date})
            if staff_attendance:
                attendance_count = len(staff_attendance.get('attendance', {}))
                presentees.append((date, attendance_count))
            else:
                presentees.append((date, 0))

        return staff_strength, presentees

    def get_student_attendance(self, week_dates):
        student_strength = Student.objects.count()
        presentees = []

        for date in week_dates:
            student_attendance = self.student_collection.find_one({'date': date})
            if student_attendance:
                attendance_count = len(student_attendance.get('attendance', {}))
                presentees.append((date, attendance_count))
            else:
                presentees.append((date, 0))

        return student_strength, presentees

    def get_student_table(self, date):
        document = self.student_collection.find_one({"date": date})
        if document:
            data = document.get("attendance", {})

            students_data = []
            for student_id, attendance_data in data.items():
                student = Student.objects.filter(id=int(student_id)).first()
                if student:
                    students_data.append({
                        'student_id': student.enrol_no,
                        'name': student.student_name,
                        'entry_time': attendance_data.get("entry_time", ""),
                        'exit_time': attendance_data.get("exit_time", "")
                    })

            return students_data
        else:
            return []

    def get_staff_table(self, date):
        document = self.staff_collection.find_one({'date': date})
        if document:
            data = document.get('attendance', {})

            staffs_data = []
            for staff_id, attendance_data in data.items():
                staff = Staff.objects.get(id=int(staff_id))
                if staff:
                    staffs_data.append({
                        'staff_id': staff.id,
                        'name': staff.username,
                        'entry_time': attendance_data.get("entry_time", ""),
                        'exit_time': attendance_data.get("exit_time", "")
                    })

            return staffs_data
        else:
            return []

# Test the DashboardManager
if __name__ == "__main__":
    # Initialize the DashboardManager with your MongoDB database name
    manager = DashboardManager("your_database_name")

    # Test getting staff attendance
    week_dates = ["2024-04-06", "2024-04-07", "2024-04-08"]
    staff_strength, staff_attendance = manager.get_staff_attendance(week_dates)
    print("Staff Strength:", staff_strength)
    print("Staff Attendance:")
    for date, count in staff_attendance:
        print(date, "-", count)

    # Test getting student attendance
    student_strength, student_attendance = manager.get_student_attendance(week_dates)
    print("\nStudent Strength:", student_strength)
    print("Student Attendance:")
    for date, count in student_attendance:
        print(date, "-", count)

    # Test getting student table for a date
    date = "2024-04-06"
    student_table = manager.get_student_table(date)
    print("\nStudent Table for", date)
    for student in student_table:
        print(student)

    # Test getting staff table for a date
    staff_table = manager.get_staff_table(date)
    print("\nStaff Table for", date)
    for staff in staff_table:
        print(staff)
