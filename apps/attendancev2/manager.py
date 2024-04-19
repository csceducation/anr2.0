import pymongo

class AttendanceManager:
    def __init__(self,mongodb_database):
        self.db_name = mongodb_database
        self.client = pymongo.MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.0")
        self.db = self.client[self.db_name]
        self.staff_collection = self.db['staff_collection']
        self.student_collection = self.db['student_collection']
        self.lab_collection = self.db['lab_collection']
        self.theory_collection = self.db['theory_collection']

    def put_lab_collection(self,lab_no,system_no,student_id,start,stop,date):
        doc = self.lab_collection.find_one({"date":date,"system_no":system_no,"lab_no":lab_no})

        if not doc:
            doc = {
                "date":date,
                "lab_no":lab_no,
                "system_no":system_no,
                "data":{
                    student_id:{
                        "start":start,
                        "stop":stop
                    }
                }
            }
        
            self.lab_collection.insert_one(doc)

        else:
            
            usage_data = {
                "start":start,
                "stop":stop
            }

            self.lab_collection.update_one(
            {"date": date,"lab_no":lab_no,"system_no":system_no},
            {"$set": {f"data.{student_id}": usage_data}})

            print("came here")


    def delete_lab_data(self, lab_no, system_no, student_id, date):
        query = {"date": date, "lab_no": lab_no, "system_no": system_no}
        update_query = {"$unset": {f"data.{student_id}": ""}}
        
        print("Query:", query)
        print("Update Query:", update_query)

        try:
            result = self.lab_collection.update_one(query, update_query)
            if result.modified_count > 0:
                print("Data deleted successfully")
            else:
                print("No matching documents found for deletion")
        except Exception as e:
            print("An error occurred:", e)


    def get_lab_data(self,lab_no,system_no,date):
        
        doc = self.lab_collection.find_one({"date":date,"lab_no":lab_no,'system_no':system_no})
    
        return doc


    def initialize_batch(self, batch_id, date,content,entry_time,exit_time,students):
        # Check if batch already exists for the given batch_id and date
        existing_batch = self.theory_collection.find_one({"batch_id": batch_id, "date": date})

        if existing_batch is None:
            document = {
                "batch_id": batch_id,
                "date": date,
                "content":content,
                "entry_time":entry_time,
                "exit_time":exit_time,
                "students": students
            }
            self.theory_collection.insert_one(document)

    def add_theory_attendance(self, batch_id, student_id, date, status, content, entry_time, exit_time):
        result = self.theory_collection.update_one(
            {"batch_id": batch_id, "date": date},
            {
                "$set": {
                    f"students.{student_id}": status,
                    "content": content,
                    "entry_time": entry_time,
                    "exit_time": exit_time
                }
            }
        )
        if result.modified_count > 0:
                print("modified")
        else:
            print("No matching documents found for for modification")

    def delete_attendance(self, batch_id, student_id, date):
        self.theory_collection.update_one(
            {"batch_id": batch_id, "date": date},
            {"$unset": {f"students.{student_id}": ""}}
        )

    def get_theory_data(self,batch,date):
        doc = self.theory_collection.find_one({"batch_id":batch,"date":date})
        return doc



class DailyAttendanceManager:
    def __init__(self, mongodb_database):
        self.db_name = mongodb_database
        self.client = pymongo.MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.0")
        self.db = self.client[self.db_name]
        self.staff_collection = self.db["staff_collection"]
        self.student_collection = self.db["student_collection"]

    def initialize_staff(self, date):
        existing_staff = self.staff_collection.find_one({"date": date})
        if existing_staff is None:
            document = {
                "date": date,
                "attendance": {}
            }
            self.staff_collection.insert_one(document)

    def add_staff_attendance(self, staff_id ,date, entry_time, exit_time,status):
        attendance_data = {
            "entry_time": entry_time,
            "exit_time": exit_time,
            "status":status
        }
        self.staff_collection.update_one(
            {"date": date},
            {"$set": {f"attendance.{staff_id}": attendance_data}}
        )

    def update_staff_attendance(self, date, entry_time, exit_time):
        attendance_data = {
            "entry_time": entry_time,
            "exit_time": exit_time
        }
        self.staff_collection.update_one(
            {"date": date},
            {"$set": {"attendance": attendance_data}}
        )

    def get_staff_attendance(self, date):
        document = self.staff_collection.find_one({"date": date})
        if document:
            return document.get("attendance", {})
        return {}

    def delete_staff_attendance(self, date,entry_number):
        self.staff_collection.update_one(
            {"date": date},
            {"$set": {f"attendance.{entry_number}": {"status":"absent","entry_time":None,"exit_time":None}}}
        )

    def initialize_student(self, date):
        existing_student = self.student_collection.find_one({"date": date})
        if existing_student is None:
            document = {
                "date": date,
                "attendance": {}
            }
            self.student_collection.insert_one(document)

    def add_student_attendance(self, student_id,date, entry_time, exit_time,status):
        attendance_data = {
            "entry_time": entry_time,
            "exit_time": exit_time,
            "status":status
        }
        self.student_collection.update_one(
            {"date": date},
            {"$set": {f"attendance.{student_id}": attendance_data}}
        )

    def update_student_attendance(self, date, entry_time, exit_time):
        attendance_data = {
            "entry_time": entry_time,
            "exit_time": exit_time
        }
        self.student_collection.update_one(
            {"date": date},
            {"$set": {"attendance": attendance_data}}
        )

    def get_student_attendance(self, date):
        document = self.student_collection.find_one({"date": date})
        if document:
            return document.get("attendance", {})
        return {}

    def delete_student_attendance(self, date, entry_number):
        print(date,entry_number)
        self.student_collection.update_one(
            {"date": date},
            {"$set": {f"attendance.{entry_number}": {"status":"absent","entry_time":None,"exit_time":None}}}
        )


