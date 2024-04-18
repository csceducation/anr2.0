import pymongo
from apps.staffs.models import Staff
from apps.students.models import Student
from apps.batch.models import BatchModel
from datetime import datetime
import certifi

class DashboardManager:
    def __init__(self, mongodb_database):
        self.client = pymongo.MongoClient('mongodb://172.18.208.1:27017/',tlsCAFile=certifi.where(),connect=False)
        self.db = self.client[mongodb_database]
        self.staff_collection = self.db["staff_collection"]
        self.student_collection = self.db["student_collection"]
        self.lab_collection = self.db['lab_collection']
        self.theory_collection = self.db['theory_collection']

    def __del__(self):
        self.client.close()

    def get_staff_attendance(self, week_dates):
        staff_strength = Staff.objects.count()
        presentees = []

        for date in week_dates:
            staff_attendance = self.staff_collection.find_one({
                'date': date,
                'attendance': {'$exists': True, '$ne': {}}
            })
            if staff_attendance:
                present_staff = {k: v for k, v in staff_attendance.get('attendance', {}).items() if v.get('entry_time') and v.get('exit_time')}
                attendance_count = len(present_staff)
                presentees.append((date, attendance_count))
            else:
                presentees.append((date, 0))

        return staff_strength, presentees


    def get_student_attendance(self, week_dates):
        student_strength = Student.objects.count()
        presentees = []

        for date in week_dates:
            student_attendance = self.student_collection.find_one({
                'date': date,
                'attendance': {'$exists': True, '$ne': {}}
            })
            if student_attendance:
                present_students = {k: v for k, v in student_attendance.get('attendance', {}).items() if v.get('entry_time') and v.get('exit_time')}
                attendance_count = len(present_students)
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


    def get_batch_dashboard(self, dates, batch):
        batch_id = batch.id

        # Get all lab documents for the given batch_id and dates
        lab_documents = self.lab_collection.find({
            'batch_id': batch_id,
            'date': {'$in': dates},
            'students': {'$exists': True, '$ne': {}}
        })

        # Get all theory documents for the given batch_id and dates
        theory_documents = self.theory_collection.find({
            'batch_id': batch_id,
            'date': {'$in': dates},
            'students': {'$exists': True, '$ne': {}}
        })

        # Create dictionaries to store presentees for each date for lab and theory
        lab_presentees = {date: 0 for date in dates}
        theory_presentees = {date: 0 for date in dates}

        # Calculate lab presentees
        for lab_doc in lab_documents:
            date = lab_doc['date']
            students = lab_doc.get('students', {})
            present_students = {k: v for k, v in students.items() if v.get('entry_time') and v.get('exit_time')}
            lab_presentees[date] += len(present_students)

        # Calculate theory presentees
        for theory_doc in theory_documents:
            date = theory_doc['date']
            students = theory_doc.get('students', {})
            present_students = {k: v for k, v in students.items() if v.get('entry_time') and v.get('exit_time')}
            theory_presentees[date] += len(present_students)

        # Combine the presentees for lab and theory into a single list of tuples
        data = [
            (date, lab_presentees[date], theory_presentees[date])
            for date in dates
        ]

        # Get the batch strength (total number of students in the batch)
        batch_strength = batch.batch_students.all().count()

        return data, batch_strength

    def get_batch_attendance(self, date, batch_id):
        lab_document = self.lab_collection.find_one({"date": date, 'batch_id': batch_id})
        theory_document = self.theory_collection.find_one({"date": date, 'batch_id': batch_id})

        students_data = []

        # Logic for Lab Collection
        if lab_document:
            lab_data = lab_document.get("students", {})
            for student_id, attendance_data in lab_data.items():
                student = Student.objects.filter(id=int(student_id)).first()
                if student:
                    student_info = {
                        'student_id': student.enrol_no,
                        'name': student.student_name,
                        'lab_entry_time': attendance_data.get("entry_time", ""),
                        'lab_exit_time': attendance_data.get("exit_time", ""),
                        'theory_entry_time': "",
                        'theory_exit_time': "",
                        'theory_status':"",
                        'lab_status':attendance_data.get("status","")
                    }
                    students_data.append(student_info)

        # Logic for Theory Collection
        if theory_document:
            theory_data = theory_document.get("students", {})
            for student_id, student_info in theory_data.items():
                student = Student.objects.filter(id=int(student_id)).first()
                if student:
                    existing_student = next((s for s in students_data if s['student_id'] == student.enrol_no), None)
                    if existing_student:
                        existing_student['theory_entry_time'] = student_info.get("entry_time", "")
                        existing_student['theory_exit_time'] = student_info.get("exit_time", "")
                        existing_student['theory_status'] = student_info.get("status","")
                    else:
                        student_info = {
                            'student_id': student.enrol_no,
                            'name': student.student_name,
                            'lab_entry_time': "",
                            'lab_exit_time': "",
                            'theory_entry_time': student_info.get("entry_time", ""),
                            'theory_exit_time': student_info.get("exit_time", ""),
                            'theory_status':student_info.get("status","")
                        }
                        students_data.append(student_info)

        return students_data

    def get_public_attendance(self,student,batch_id):
        pipeline = [
            {"$match": {"batch_id": batch_id}},
            {"$sort": {"date": 1}} 
        ]

        lab_documents = list(self.lab_collection.aggregate(pipeline))
        theory_documents = list(self.theory_collection.aggregate(pipeline))
        
        return create_student_data(student,lab_documents,theory_documents,batch_id)

    def get_batch_summary(self, batch):
        batch_id = batch.id

        # Get all lab documents for the given batch_id and dates
        lab_documents = self.lab_collection.find({
            'batch_id': batch_id,
            'students': {'$exists': True, '$ne': {}}
        })

        # Get all theory documents for the given batch_id and dates
        theory_documents = self.theory_collection.find({
            'batch_id': batch_id,
            'students': {'$exists': True, '$ne': {}}
        })

        # Create dictionaries to store the total students present for each date
        lab_students_per_date = {}
        theory_students_per_date = {}

        # Process lab documents
        for lab_doc in lab_documents:
            date = lab_doc.get('date')
            students_present = sum(1 for student in lab_doc['students'].values() if student['status'] == 'present')
            lab_students_per_date[date] = lab_students_per_date.get(date, 0) + students_present

        # Process theory documents
        for theory_doc in theory_documents:
            date = theory_doc.get('date')
            students_present = sum(1 for student in theory_doc['students'].values() if student['status'] == 'present')
            theory_students_per_date[date] = theory_students_per_date.get(date, 0) + students_present

        return {
            'lab_students_per_date': lab_students_per_date,
            'theory_students_per_date': theory_students_per_date
        }
        
    def get_staff_summary(self,staff,month,year):
        staff_id = str(staff.id)
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
        # Query for the specific month
        query = {
            "date": {
                "$gte": str(start_date.date()),
                "$lt": str(end_date.date())
            }
        }

        # Fetch documents
        results = self.staff_collection.find(query)
        
        summary = []
        for result in results:
            data = {}
            data['date'] = result['date']
            data['status'] = result.get("atttendance",{}).get(staff_id,{}).get('status',"present")
            data["entry"] = result.get("attendance",{}).get(staff_id,{}).get("entry_time","N/A")
            data["exit"] = result.get("attendance",{}).get(staff_id,{}).get("exit_time","N/A")
            summary.append(data)
        
        return summary
        '''
        data = []
        # Loop through documents and print all data
        for result in results:
            obj = {}
            obj['id'] = result["_id"]
            obj["date"] = result['date']
            obj['attendance'] = result['attendance']
            data.append(obj)
            #print("Document ID:", result["_id"])
            #print("Date:", result["date"])
            #print("Attendance Data:")
            #for staff_id, data in result["attendance"].items():
            #    print("  Staff ID:", staff_id)
            #    print("  Entry Time:", data["entry_time"])
            #    print("  Exit Time:", data["exit_time"])
            #    print("  Status:", data["status"].capitalize() if data["status"] else "Unknown")
            #    print()
            #print("-" * 50)
        return data
        '''

def create_student_data(student_id, lab_documents, theory_documents,batch_id):
    student_lab_data = []
    student_theory_data = []
    batch = BatchModel.objects.get(id=batch_id)
    for lab_doc in lab_documents:
        if str(student_id) in lab_doc['students']:
            student_lab_data.append({
                'date': lab_doc['date'],
                'entry_time': lab_doc['students'][str(student_id)].get('entry_time', ''),
                'exit_time': lab_doc['students'][str(student_id)].get('exit_time', ''),
                'system_no': lab_doc['students'][str(student_id)].get('system_no', '')
            })

    for theory_doc in theory_documents:
        if str(student_id) in theory_doc.get('students', {}):
            student_theory_data.append({
                'date': theory_doc['date'],
                'content': theory_doc.get('content', ''),
                'entry_time': theory_doc['students'][str(student_id)].get('entry_time', ''),
                'exit_time': theory_doc['students'][str(student_id)].get('exit_time', ''),
                'status': theory_doc['students'][str(student_id)].get('status', ''),
            })
        
    data = {
        "batch_info":{
            "batch_id":batch.batch_id,
            "batch_subject":batch.batch_course.name,
            "batch_staff":batch.batch_staff.username
        },
        "lab":student_lab_data,
        "theory":student_theory_data
    }

    return data


    