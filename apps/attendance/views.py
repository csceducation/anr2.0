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


connection_string = "mongodb://172.18.208.1:27017/"
db = "anr_attendance"
lab_collection = "lab_collection"
theory_collection = "theory_collection"
staff_colletion = "staff_collection"
student_colletion = "student_collection"


def lab_attendance(request, batch_id):
    batch = get_object_or_404(BatchModel, id=batch_id)
    manager = AttendanceManager(connection_string, db, lab_collection)
    
    if 'date' in request.GET and 'entrytime' in request.GET and 'exittime' in request.GET:
        date = request.GET.get('date')
        p_entry_time = request.GET.get('entrytime')
        p_exit_time = request.GET.get('exittime')
    else:
        
        if request.method == 'POST':
            form = DateForm(request.POST)
            form.fields.pop('content')
            if form.is_valid():
                date = form.cleaned_data['date']
                entrytime = form.cleaned_data['entrytime']
                exittime = form.cleaned_data['exittime']
                return HttpResponseRedirect(request.path + f"?date={date}&entrytime={entrytime}&exittime={exittime}")
        else:
            form = DateForm()
            form.fields.pop('content')
        return render(request, 'date_form.html', {'form': form})
    
    manager.initialize_batch(batch_id,date)
    existing_data = manager.get_attendance(batch_id, date)

    if request.method == 'POST':
        for student in batch.batch_students.all():
            student_id = student.id
            entry_time = request.POST.get(f'entry_time_{student_id}')
            exit_time = request.POST.get(f'exit_time_{student_id}')
            status = request.POST.get(f"status_{student_id}")
            system_no = request.POST.get(f"system_no_{student_id}")
            manager.update_attendance(batch_id, student_id, date, entry_time, exit_time,status,system_no)

        redirect_url = reverse('lab_attendance', kwargs={'batch_id': batch_id}) + f'?date={date}'
        return HttpResponseRedirect(redirect_url)
    
    
    students_data = []
    for student in batch.batch_students.all():
        student_id = student.id
        student_data = {
            'student_id': student_id,
            'name': student.student_name,
            'entry_time': existing_data.get(str(student_id),{}).get("entry_time",""),
            'exit_time': existing_data.get(str(student_id),{}).get("exit_time",""),
            'status':existing_data.get(str(student_id),{}).get('status',""),
            'system_no':existing_data.get(str(student_id),{}).get('system_no',""),

        }
        students_data.append(student_data)
    
    context = {
        'batch': batch,
        'date': date,
        'students_data': students_data,
        'entry_time':p_entry_time,
        'exit_time':p_exit_time,
    }
    
    return render(request, 'lab_attendance_form.html', context)

def delete_lab_attendance(request,**kwargs):
    batch_id = kwargs.get("batch_id","")
    date = kwargs.get("date","")
    student_id = kwargs.get("stud_id")
    manager = AttendanceManager(connection_string, db, lab_collection)
    manager.delete_attendance(batch_id=batch_id,date=date,student_id=student_id)
    return redirect(request.META.get('HTTP_REFERER', '/'))



def theory_attendance(request, batch_id):
    batch = get_object_or_404(BatchModel, id=batch_id)
    manager = AttendanceManager(connection_string, db, theory_collection)

    if 'date' in request.GET and 'entrytime' in request.GET and 'exittime' in request.GET:
        date = request.GET.get('date')
        p_entry_time = request.GET.get('entrytime')
        p_exit_time = request.GET.get('exittime')
    else:
        
        if request.method == 'POST':
            form = DateForm(request.POST)
            if form.is_valid():
                date = form.cleaned_data['date']
                content = form.cleaned_data['content']
                date_string = date.strftime("%Y-%m-%d")
                manager.initialize_batch(batch_id,date_string,content)
                entrytime = form.cleaned_data['entrytime']
                exittime = form.cleaned_data['exittime']
                return HttpResponseRedirect(request.path + f"?date={date}&entrytime={entrytime}&exittime={exittime}")
        else:
            form = DateForm()
        return render(request, 'date_form.html', {'form': form})

    
    existing_data = manager.get_attendance(batch_id, date)

    if request.method == 'POST':
        for student in batch.batch_students.all():
            student_id = student.id
            entry_time = request.POST.get(f'entry_time_{student_id}')
            exit_time = request.POST.get(f'exit_time_{student_id}')
            status = request.POST.get(f"status_{student_id}")
            
            manager.add_attendance(batch_id, student_id, date, entry_time, exit_time,status)

        redirect_url = reverse('theory_attendance', kwargs={'batch_id': batch_id}) + f'?date={date}'
        return HttpResponseRedirect(redirect_url)
    
    
    students_data = []
    for student in batch.batch_students.all():
        student_id = student.id
        student_data = {
            'student_id': student_id,
            'name': student.student_name,
            'entry_time': existing_data.get(str(student_id),{}).get("entry_time",""),
            'exit_time': existing_data.get(str(student_id),{}).get("exit_time",""),
            'status':existing_data.get(str(student_id),{}).get('status',"")
        }
        students_data.append(student_data)
    
    context = {
        'batch': batch,
        'date': date,
        'students_data': students_data,
        'entry_time':p_entry_time,
        'exit_time':p_exit_time,
    }
    
    return render(request, 'theory_attendance_form.html', context)

def delete_theory_attendance(request,**kwargs):
    batch_id = kwargs.get("batch_id","")
    date = kwargs.get("date","")
    student_id = kwargs.get("stud_id")
    manager = AttendanceManager(connection_string, db, theory_collection)
    manager.delete_attendance(batch_id=batch_id,date=date,student_id=student_id)
    return redirect(request.META.get('HTTP_REFERER', '/'))


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
            status = request.POST.get(f"status_{staff.id}")
            
            manager.add_staff_attendance(student_id, date, entry_time, exit_time,status)

        redirect_url = reverse('staff_attendance') + f'?date={date}'
        return HttpResponseRedirect(redirect_url)

    staffs_data = []
    
    
    for staff in staff_queryset:
        staffs_data.append({
            'staff_id': staff.id,
            'name': staff.username,
            'entry_time': existing_data.get(str(staff.id), {}).get("entry_time", ""),
            'exit_time': existing_data.get(str(staff.id), {}).get("exit_time", ""),
            'status':existing_data.get(str(staff.id),{}).get('status',"")
        })

    context = {
        'date': date,
        'staffs_data': staffs_data,
    }

    return render(request, 'staff_attendance.html', context)


def delete_staff_attendance(request,**kwargs):
    date = kwargs.get("date","")
    staff_id = kwargs.get("staff_id","")
    manager = DailyAttendanceManager(connection_string, db, staff_colletion)
    manager.delete_staff_attendance(date,str(staff_id))
    return redirect(request.META.get('HTTP_REFERER', '/'))

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
            status = request.POST.get(f"status_{student.id}")
            
            manager.add_student_attendance(student_id, date, entry_time, exit_time,status)

        redirect_url = reverse('student_attendance') + f'?date={date}'
        return HttpResponseRedirect(redirect_url)

    students_data = []
    
    
    for student in student_queryset:
        students_data.append({
            'student_id': student.id,
            'name': student.student_name,
            'entry_time': existing_data.get(str(student.id), {}).get("entry_time", ""),
            'exit_time': existing_data.get(str(student.id), {}).get("exit_time", ""),
            'status': existing_data.get(str(student.id), {}).get("status", "")
        })

    context = {
        'date': date,
        'students_data': students_data,
    }

    return render(request, 'student_attendance.html', context)

def delete_student_attendance(request,**kwargs):
    date = kwargs.get("date","")
    student_id = kwargs.get("student_id","")
    manager = DailyAttendanceManager(connection_string, db, student_colletion)
    manager.delete_staff_attendance(date,str(student_id))
    return redirect(request.META.get('HTTP_REFERER', '/'))


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
    

def batch_dashboard(request, *args,**kwargs):
    selected_week = request.GET.get('week',None)
    date = request.GET.get('date',None)
    staff_id = request.GET.get('staff_id',None)
    if staff_id == None:
        staffs = Staff.objects.all()
        return render(request,'not_selected.html',{'staffs':staffs})
    staff = Staff.objects.get(id=staff_id)
    batches = BatchModel.objects.filter(batch_staff=staff,)
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
    manager = DashboardManager(db)
    graphs = []
    presentees =[]
    for batch in batches:
        data,strength = manager.get_batch_dashboard(dates,batch)
        presentees.append({batch.batch_id:data})
        student_trace1 = {
            'x': dates,
            'y': [item[1] for item in data],
            'name': 'Student Presentees - Lab',
            'type': 'bar'
        }
        student_trace2 = {
            'x': dates,
            'y': [item[2] for item in data],
            'name': 'Student Presentees - Theory',
            'type': 'bar'
        }
        student_trace3 = {
            'x': dates,
            'y': [strength for _ in range(len(dates))],
            'name': 'Student Strength',
            'type': 'bar'
        }
        
        student_data = [student_trace1, student_trace2, student_trace3]
        student_layout = {
            'title': f'Student Attendance for batch : {batch.batch_id} batch subject : {batch.batch_course}' ,
            'barmode': 'group'
        }
        student_fig = {
            'data': student_data,
            'layout': student_layout
        }
        student_graphJSON = json.dumps(student_fig)
        graphs.append(student_graphJSON)
        #print(data)
    
    batch_id = request.GET.get('batch_id',None)
    
    if batch_id ==  None:
        return render(request,"batch_dashboard.html",{"graphs":graphs,"week_dates":dates,'batches':batches})
    
    table = manager.get_batch_attendance(date,int(batch_id))
    batch = BatchModel.objects.get(id=batch_id)
    if date == None:
        return render(request,"batch_dashboard.html",{"graphs":graphs,"week_dates":dates,"table":table,'batches':batches,'batch':batch,'date':date})
    
    if date != None:
        total_presentees_lab,total_presentees_theory,total_strength = extract_totals(graphs,date)
        metrics = {
            "total_strength":total_strength,
            "total_lab_presentees":total_presentees_lab,
            "total_theory_presentees":total_presentees_theory
        }
        return render(request,"batch_dashboard.html",{"graphs":graphs,"week_dates":dates,"table":table,'batches':batches,'batch':batch,'date':date,'metrics':metrics})

    #table = manager.get_batch_attendance(date,int(batch_id))
    #batch = BatchModel.objects.get(id=batch_id)
    #return render(request,"batch_dashboard.html",{"graphs":graphs,"week_dates":dates,"table":table,'batches':batches,'batch':batch,'date':date})
    #return JsonResponse(graphs,safe=False,status=200)



def extract_totals(data, target_date):
    for json_str in data:
        # Parse the JSON string
        parsed_json = json.loads(json_str)

        # Get the x values (dates) and y values (attendance)
        x_values = parsed_json['data'][0]['x']
        y_values_presentees_lab = parsed_json['data'][0]['y']
        y_values_presentees_theory = parsed_json['data'][1]['y']
        y_values_strength = parsed_json['data'][2]['y']

        # Find the index of the target date
        try:
            index = x_values.index(target_date)
        except ValueError:
            print(f"Date {target_date} not found in the data.")
            continue

        # Get the total strength and total presentees for the target date
        total_strength = y_values_strength[index]
        total_presentees_lab = y_values_presentees_lab[index]
        total_presentees_theory = y_values_presentees_theory[index]

        return total_presentees_lab,total_presentees_theory,total_strength



def provide_batch_summary(batch):
    manager = DashboardManager(db)
    data = manager.get_batch_summary(batch)
    #print(data)
    return data
    #return JsonResponse("success",safe=False,status=200)

def provide_staff_summary(staff,month,year):
    manager = DashboardManager(db)
    data = manager.get_staff_summary(staff,month,year)
    #print(data)
    return data