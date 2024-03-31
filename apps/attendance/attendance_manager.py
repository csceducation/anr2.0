# attendance_manager.py

import pymongo

class AttendanceManager:
    def __init__(self, mongodb_uri, mongodb_database,collection_name):
        self.db_name = mongodb_database
        self.client = pymongo.MongoClient(mongodb_uri)
        self.db = self.client[self.db_name]
        self.collection = self.db[collection_name]

    def initialize_batch(self, batch_id, date):
        # Check if batch already exists for the given batch_id and date
        existing_batch = self.collection.find_one({"batch_id": batch_id, "date": date})
        if existing_batch is None:
            document = {
                "batch_id": batch_id,
                "date": date,
                "students": {}
            }
            self.collection.insert_one(document)

    def add_attendance(self, batch_id, student_id, date, entry_time, exit_time):
        attendance_data = {
            "entry_time": entry_time,
            "exit_time": exit_time
        }
        self.collection.update_one(
            {"batch_id": batch_id, "date": date},
            {"$set": {f"students.{student_id}": attendance_data}}
        )

    def update_attendance(self, batch_id, student_id, date, entry_time, exit_time):
        attendance_data = {
            "entry_time": entry_time,
            "exit_time": exit_time
        }
        self.collection.update_one(
            {"batch_id": batch_id, "date": date},
            {"$set": {f"students.{student_id}": attendance_data}}
        )

    def get_attendance(self, batch_id, date):
        document = self.collection.find_one({"batch_id": batch_id, "date": date})
        if document:
            return document.get("students", {})
        return {}

    def delete_attendance(self, batch_id, student_id, date):
        self.collection.update_one(
            {"batch_id": batch_id, "date": date},
            {"$unset": {f"students.{student_id}": ""}}
        )

class DailyAttendanceManager:
    def __init__(self, mongodb_uri, mongodb_database, attendance_collection_name):
        self.db_name = mongodb_database
        self.client = pymongo.MongoClient(mongodb_uri)
        self.db = self.client[self.db_name]
        self.attendance_collection = self.db[attendance_collection_name]

    def initialize_staff(self, date):
        existing_staff = self.attendance_collection.find_one({"date": date})
        if existing_staff is None:
            document = {
                "date": date,
                "attendance": {}
            }
            self.attendance_collection.insert_one(document)

    def add_staff_attendance(self, staff_id ,date, entry_time, exit_time):
        attendance_data = {
            "entry_time": entry_time,
            "exit_time": exit_time
        }
        self.attendance_collection.update_one(
            {"date": date},
            {"$set": {f"attendance.{staff_id}": attendance_data}}
        )

    def update_staff_attendance(self, date, entry_time, exit_time):
        attendance_data = {
            "entry_time": entry_time,
            "exit_time": exit_time
        }
        self.attendance_collection.update_one(
            {"date": date},
            {"$set": {"attendance": attendance_data}}
        )

    def get_staff_attendance(self, date):
        document = self.attendance_collection.find_one({"date": date})
        if document:
            return document.get("attendance", {})
        return {}

    def delete_staff_attendance(self, date):
        self.attendance_collection.update_one(
            {"date": date},
            {"$unset": {"attendance": ""}}
        )

    def initialize_student(self, date):
        existing_student = self.attendance_collection.find_one({"date": date})
        if existing_student is None:
            document = {
                "date": date,
                "attendance": {}
            }
            self.attendance_collection.insert_one(document)

    def add_student_attendance(self, student_id,date, entry_time, exit_time):
        attendance_data = {
            "entry_time": entry_time,
            "exit_time": exit_time
        }
        self.attendance_collection.update_one(
            {"date": date},
            {"$set": {f"attendance.{student_id}": attendance_data}}
        )

    def update_student_attendance(self, date, entry_time, exit_time):
        attendance_data = {
            "entry_time": entry_time,
            "exit_time": exit_time
        }
        self.attendance_collection.update_one(
            {"date": date},
            {"$set": {"attendance": attendance_data}}
        )

    def get_student_attendance(self, date):
        document = self.attendance_collection.find_one({"date": date})
        if document:
            return document.get("attendance", {})
        return {}

    def delete_student_attendance(self, date):
        self.attendance_collection.update_one(
            {"date": date},
            {"$unset": {"attendance": ""}}
        )