from django.db import models
from apps.batch.models import BatchModel
from apps.course.models import CourseModel
from apps.students.models import Student
from apps.staffs.models import Staff
from django.utils import timezone

class BatchLabAttendance(models.Model):
    student = models.ForeignKey(Student, related_name='batch_lab_attendance', on_delete=models.PROTECT)
    date = models.DateField(default=timezone.now)
    session = models.IntegerField(blank=False, null=False)
    batch = models.ForeignKey(BatchModel, related_name='lab_attendance', on_delete=models.CASCADE)
    entry_time = models.TimeField()
    exit_time = models.TimeField()

    '''def clean(self):
        if BatchLabAttendance.objects.filter(student=self.student, batch=self.batch, date=self.date, session=self.session).exists():
            raise ValidationError('An attendance object for this student, batch, and date already exists.')
'''

    

class BatchTheoryAttendance(models.Model):
    student = models.ForeignKey(Student, related_name='batch_Theory_attendance', on_delete=models.PROTECT)
    date = models.DateField(default=timezone.now)
    session = models.IntegerField(blank=False, null=False)
    batch = models.ForeignKey(BatchModel, related_name='Theory_attendance', on_delete=models.CASCADE)
    entry_time = models.TimeField()
    exit_time = models.TimeField()


class DailyAttendance(models.Model):
    students = models.ManyToManyField(Student)
    date = models.DateField(auto_now=True,unique=True)


class StaffDailyAttendance(models.Model):
    staffs = models.ManyToManyField(Staff)
    date = models.DateField(auto_now=True,unique=True)

from datetime import date

class BatchLabAttendanceSummary:
    def __init__(self, batch_model, date, session=None):
        self.batch_model = batch_model
        self.date = date
        self.session = session

    def get_attendance_summary(self, date=None, session=None):
        batch_data = {}
        date = date or self.date
        session = session or self.session

        if session is None:
            sessions = BatchLabAttendance.objects.filter(batch=self.batch_model, date=date).values_list('session', flat=True).distinct()
            session_data = {}

            for sn in sessions:
                attendances = BatchLabAttendance.objects.filter(batch=self.batch_model, date=date, session=sn)
                session_attendance = []
                
                for attendance in attendances:
                    data = {
                        "student": attendance.student,
                        "entry": attendance.entry_time,
                        "exit": attendance.exit_time
                    }
                    session_attendance.append(data)

                session_data[sn] = session_attendance

            batch_data[self.batch_model.batch_course.name] = session_data

        elif session:
            session_data = {}
            attendances = BatchLabAttendance.objects.filter(batch=self.batch_model, date=date, session=session)
            session_attendance = []
            
            for attendance in attendances:
                data = {
                    "student": attendance.student,
                    "entry": attendance.entry_time,
                    "exit": attendance.exit_time
                }
                session_attendance.append(data)

            session_data[session] = session_attendance
            batch_data[self.batch_model.batch_course.name] = session_data

        return batch_data


class BatchTheoryAttendanceSummary:
    def __init__(self, batch_model, date, session=None):
        self.batch_model = batch_model
        self.date = date
        self.session = session

    def get_attendance_summary(self, date=None, session=None):
        batch_data = {}
        date = date or self.date
        session = session or self.session

        if session is None:
            sessions = BatchTheoryAttendance.objects.filter(batch=self.batch_model, date=date).values_list('session', flat=True).distinct()
            session_data = {}

            for sn in sessions:
                attendances = BatchTheoryAttendance.objects.filter(batch=self.batch_model, date=date, session=sn)
                session_attendance = []
                
                for attendance in attendances:
                    data = {
                        "student": attendance.student,
                        "entry": attendance.entry_time,
                        "exit": attendance.exit_time
                    }
                    session_attendance.append(data)

                session_data[sn] = session_attendance

            batch_data[self.batch_model.batch_course.name] = session_data

        elif session:
            session_data = {}
            attendances = BatchTheoryAttendance.objects.filter(batch=self.batch_model, date=date, session=session)
            session_attendance = []
            
            for attendance in attendances:
                data = {
                    "student": attendance.student,
                    "entry": attendance.entry_time,
                    "exit": attendance.exit_time
                }
                session_attendance.append(data)

            session_data[session] = session_attendance
            batch_data[self.batch_model.batch_course.name] = session_data

        return batch_data
