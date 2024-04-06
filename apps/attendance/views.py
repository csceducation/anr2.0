from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.http import HttpResponseRedirect,JsonResponse
from apps.batch.models import BatchModel
from .forms import DateForm
from .attendance_manager import AttendanceManager,DailyAttendanceManager  # Import your AttendanceManager
from apps.staffs.models import Staff
from apps.students.models import Student
from .dashboard import DashboardManager
import random,json
from datetime import datetime,timedelta
import plotly.express as px


connection_string = "mongodb://localhost:27017/"
db = "anr_attendance"
lab_collection = "lab_collection"
theory_collection = "theory_collection"
staff_colletion = "staff_collection"
student_colletion = "student_collection"


def lab_attendance(request, batch_id):
    batch = get_object_or_404(BatchModel, id=batch_id)
    manager = AttendanceManager(connection_string, db, lab_collection)
    
    if 'date' in request.GET:
        date = request.GET.get('date')
    else:
        
        if request.method == 'POST':
            form = DateForm(request.POST)
            if form.is_valid():
                date = form.cleaned_data['date']
                return HttpResponseRedirect(request.path + f"?date={date}")
        else:
            form = DateForm()
        return render(request, 'date_form.html', {'form': form})
    
    manager.initialize_batch(batch_id,date)
    existing_data = manager.get_attendance(batch_id, date)

    if request.method == 'POST':
        for student in batch.batch_students.all():
            student_id = student.id
            entry_time = request.POST.get(f'entry_time_{student_id}')
            exit_time = request.POST.get(f'exit_time_{student_id}')

            
            manager.add_attendance(batch_id, student_id, date, entry_time, exit_time)

        redirect_url = reverse('lab_attendance', kwargs={'batch_id': batch_id}) + f'?date={date}'
        return HttpResponseRedirect(redirect_url)
    
    
    students_data = []
    for student in batch.batch_students.all():
        student_id = student.id
        student_data = {
            'student_id': student_id,
            'name': student.student_name,
            'entry_time': existing_data.get(str(student_id),{}).get("entry_time",""),
            'exit_time': existing_data.get(str(student_id),{}).get("exit_time","")
        }
        students_data.append(student_data)
    
    context = {
        'batch': batch,
        'date': date,
        'students_data': students_data,
    }
    
    return render(request, 'lab_attendance_form.html', context)


def theory_attendance(request, batch_id):
    batch = get_object_or_404(BatchModel, id=batch_id)
    manager = AttendanceManager(connection_string, db, theory_collection)

    if 'date' in request.GET:
        date = request.GET.get('date')
    else:
        
        if request.method == 'POST':
            form = DateForm(request.POST)
            if form.is_valid():
                date = form.cleaned_data['date']
                return HttpResponseRedirect(request.path + f"?date={date}")
        else:
            form = DateForm()
        return render(request, 'date_form.html', {'form': form})

    manager.initialize_batch(batch_id,date)
    existing_data = manager.get_attendance(batch_id, date)

    if request.method == 'POST':
        for student in batch.batch_students.all():
            student_id = student.id
            entry_time = request.POST.get(f'entry_time_{student_id}')
            exit_time = request.POST.get(f'exit_time_{student_id}')

            
            manager.add_attendance(batch_id, student_id, date, entry_time, exit_time)

        redirect_url = reverse('theory_attendance', kwargs={'batch_id': batch_id}) + f'?date={date}'
        return HttpResponseRedirect(redirect_url)
    
    
    students_data = []
    for student in batch.batch_students.all():
        student_id = student.id
        student_data = {
            'student_id': student_id,
            'name': student.student_name,
            'entry_time': existing_data.get(str(student_id),{}).get("entry_time",""),
            'exit_time': existing_data.get(str(student_id),{}).get("exit_time","")
        }
        students_data.append(student_data)
    
    context = {
        'batch': batch,
        'date': date,
        'students_data': students_data,
    }
    
    return render(request, 'theory_attendance_form.html', context)



def staff_attendance(request):
    manager = DailyAttendanceManager(connection_string, db, staff_colletion)

    if 'date' in request.GET:
        date = request.GET.get('date')
    else:
        if request.method == 'POST':
            form = DateForm(request.POST)
            if form.is_valid():
                date = form.cleaned_data['date']
                return HttpResponseRedirect(request.path + f"?date={date}")
        else:
            form = DateForm()
        return render(request, 'date_form.html', {'form': form})

    manager.initialize_staff(date)
    existing_data = manager.get_staff_attendance(date)
    staff_queryset = Staff.objects.all()
    if request.method == 'POST':
        for staff in staff_queryset:
            student_id = staff.id
            entry_time = request.POST.get(f'entry_time_{staff.id}')
            exit_time = request.POST.get(f'exit_time_{staff.id}')

            
            manager.add_staff_attendance(student_id, date, entry_time, exit_time)

        redirect_url = reverse('staff_attendance') + f'?date={date}'
        return HttpResponseRedirect(redirect_url)

    staffs_data = []
    
    
    for staff in staff_queryset:
        staffs_data.append({
            'staff_id': staff.id,
            'name': staff.username,
            'entry_time': existing_data.get(str(staff.id), {}).get("entry_time", ""),
            'exit_time': existing_data.get(str(staff.id), {}).get("exit_time", "")
        })

    context = {
        'date': date,
        'staffs_data': staffs_data,
    }

    return render(request, 'staff_attendance.html', context)


def student_attendance(request):
    manager = DailyAttendanceManager(connection_string, db, student_colletion)

    if 'date' in request.GET:
        date = request.GET.get('date')
    else:
        if request.method == 'POST':
            form = DateForm(request.POST)
            if form.is_valid():
                date = form.cleaned_data['date']
                return HttpResponseRedirect(request.path + f"?date={date}")
        else:
            form = DateForm()
        return render(request, 'date_form.html', {'form': form})

    manager.initialize_student(date)
    existing_data = manager.get_student_attendance(date)
    student_queryset = Student.objects.all()
    if request.method == 'POST':
        for student in student_queryset:
            student_id = student.id
            entry_time = request.POST.get(f'entry_time_{student.id}')
            exit_time = request.POST.get(f'exit_time_{student.id}')

            
            manager.add_student_attendance(student_id, date, entry_time, exit_time)

        redirect_url = reverse('student_attendance') + f'?date={date}'
        return HttpResponseRedirect(redirect_url)

    students_data = []
    
    
    for student in student_queryset:
        students_data.append({
            'student_id': student.id,
            'name': student.student_name,
            'entry_time': existing_data.get(str(student.id), {}).get("entry_time", ""),
            'exit_time': existing_data.get(str(student.id), {}).get("exit_time", "")
        })

    context = {
        'date': date,
        'students_data': students_data,
    }

    return render(request, 'student_attendance.html', context)


def router(request):
    return render(request,'router.html')

def day_dashboard(request, *args):
    selected_week = request.GET.get('week')
    date = request.GET.get('date')

    if selected_week:
        year, week_num = map(int, selected_week.split('-W'))
        first_day_of_week = datetime.strptime(f'{year}-W{week_num}-1', "%Y-W%W-%w")
    else:
        # If 'week' parameter is not provided, use the current week
        today = datetime.now()
        year, week_num, _ = today.isocalendar()
        first_day_of_week = today - timedelta(days=today.weekday())  # Start of the current week

    dates = []
    for i in range(7):
        day = first_day_of_week + timedelta(days=i)
        if day.weekday() != 6:
            dates.append(day.strftime('%Y-%m-%d'))  # Format date as 'yy-mm-dd'

    if date is None:
        date = dates[0]

    manager = DashboardManager(db)
    staff_strength, staff_presentees = manager.get_staff_attendance(dates)
    student_strength, students_presentees = manager.get_student_attendance(dates)

    students_data = manager.get_student_table(date)
    staffs_data = manager.get_staff_table(date)

    
    staff_trace1 = {
        'x': dates,
        'y': [item[1] for item in staff_presentees],
        'name': 'Staff Presentees',
        'type': 'bar'
    }
    staff_trace2 = {
        'x': dates,
        'y': [staff_strength for _ in range(len(dates))],
        'name': 'Staff Strength',
        'type': 'bar'
    }
    staff_data = [staff_trace1, staff_trace2]
    staff_layout = {
        'title': 'Staff Attendance',
        'barmode': 'group'
    }
    staff_fig = {
        'data': staff_data,
        'layout': staff_layout
    }

    # Create the bar chart for students
    student_trace1 = {
        'x': dates,
        'y': [item[1] for item in students_presentees],
        'name': 'Student Presentees',
        'type': 'bar'
    }
    student_trace2 = {
        'x': dates,
        'y': [student_strength for _ in range(len(dates))],
        'name': 'Student Strength',
        'type': 'bar'
    }
    student_data = [student_trace1, student_trace2]
    student_layout = {
        'title': 'Student Attendance',
        'barmode': 'group'
    }
    student_fig = {
        'data': student_data,
        'layout': student_layout
    }
    staff_graphJSON = json.dumps(staff_fig)
    student_graphJSON = json.dumps(student_fig)
    context = {
        'students_data': students_data,
        'staffs_data': staffs_data,
        'week_dates': dates,
        'staff_graphJSON': staff_graphJSON,
        'student_graphJSON': student_graphJSON,

    }
    return render(request, 'day_dashboard.html', context)
    

def batch_dashboard(request):
    return JsonResponse('hello',safe=False,status=200)