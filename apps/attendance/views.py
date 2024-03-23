from django.shortcuts import render, redirect,get_object_or_404
from .models import BatchLabAttendance,BatchTheoryAttendance,DailyAttendance,StaffDailyAttendance,BatchLabAttendanceSummary,BatchTheoryAttendanceSummary
from apps.batch.models import BatchModel
from apps.students.models import Student
from datetime import datetime
from .forms import BatchLabAttendanceForm,BatchTheoryAttendanceForm,DailyAttendanceForm,StaffDailyAttendanceForm,DashboardForm
from django.views import View
from django.http import HttpResponse,Http404
from apps.staffs.models import Staff
from django.utils import timezone

current_date = datetime.now().date()

def lab_attendance_for_batch(request,*args,**kwargs):
    pk = kwargs.get("pk")
    batch = BatchModel.objects.get(id=pk)
    attendances = BatchLabAttendance.objects.filter(batch=batch,date=current_date)

    return render(request,'batch_lab_attendances.html',{'attendances':attendances,"batch":batch})



def lab_attendance_form(request, *args, **kwargs):
    batch_id = kwargs.get("batch_id")
    session = kwargs.get("session")
    date_str = kwargs.get("date")
    date = datetime.strptime(date_str, "%Y-%m-%d").date()

    batch = get_object_or_404(BatchModel, id=batch_id)
    students = batch.batch_students.all()
    
    forms = []
    
    for student in students:
        try:
            attendance = BatchLabAttendance.objects.get(batch=batch, date=date, session=session, student=student)
        except BatchLabAttendance.DoesNotExist:
            form = BatchLabAttendanceForm(initial={
                'student_id': student.id,
                'batch_id': batch.id,
                'session': session,
                'date': date,
            })
        else:
            form = BatchLabAttendanceForm(instance=attendance,initial={
                'student_id': student.id,
                'batch_id': batch.id,
                'session': session,
                'date': date,
            })

        student_form = {
            "form": form,
            "student": student
        }
        forms.append(student_form)

    
    context = {
        "forms":forms,
        'batch_id': batch_id,
        'session': session,
        'date': date,
    }
    return render(request, 'fill_lab_attendance.html', context)


def add_update_lab_attendance(request, *args, **kwargs):
    if request.method == 'POST':
        batch_id = request.POST.get("batch_id")
        session = request.POST.get("session")
        student_id =request.POST.get('student_id') 
        date_str = request.POST.get("date")
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        student=Student.objects.get(id=student_id)
        batch = get_object_or_404(BatchModel, id=batch_id)
        try:
            attendance = BatchLabAttendance.objects.get(batch=batch,student=student,date=date,session=session)
            attendance.entry_time=request.POST.get('entry_time')
            attendance.exit_time=request.POST.get('exit_time')
            attendance.save()
            return redirect('lab_attendance_form',batch_id=batch_id,date=date_str,session=session)
        except BatchLabAttendance.DoesNotExist:
            attendnace = BatchLabAttendance.objects.create
            attendnace = BatchLabAttendance.objects.create(batch=batch,student=student,date=date,session=session,entry_time=request.POST.get('entry_time'),exit_time=request.POST.get('exit_time'))
            attendnace.save()
            return redirect('lab_attendance_form',batch_id=batch_id,date=date_str,session=session)

def delete_lab_attendance(request, *args, **kwargs):
    batch_id = kwargs.get("batch_id")
    session = kwargs.get("session")
    date_str = kwargs.get("date")
    date = datetime.strptime(date_str, "%Y-%m-%d").date()

    batch = get_object_or_404(BatchModel, id=batch_id)

    objects = BatchLabAttendance.objects.filter(batch=batch,session=session,date=date)
    objects.delete()
    return redirect('lab_attendance', pk=batch_id)


def Theory_attendance_for_batch(request,*args,**kwargs):
    pk = kwargs.get("pk")
    batch = BatchModel.objects.get(id=pk)
    attendances = BatchTheoryAttendance.objects.filter(batch=batch)

    return render(request,'batch_theory_attendances.html',{'attendances':attendances,"batch":batch})



def Theory_attendance_form(request, *args, **kwargs):
    batch_id = kwargs.get("batch_id")
    session = kwargs.get("session")
    date_str = kwargs.get("date")
    date = datetime.strptime(date_str, "%Y-%m-%d").date()

    batch = get_object_or_404(BatchModel, id=batch_id)
    students = batch.batch_students.all()
    
    forms = []
    
    for student in students:
        try:
            attendance = BatchTheoryAttendance.objects.get(batch=batch, date=date, session=session, student=student)
        except BatchTheoryAttendance.DoesNotExist:
            
            form = BatchTheoryAttendanceForm(initial={
                'student_id': student.id,
                'batch_id': batch.id,
                'session': session,
                'date': date,
            })
        else:
             form = BatchTheoryAttendanceForm(instance=attendance,initial={
                'student_id': student.id,
                'batch_id': batch.id,
                'session': session,
                'date': date,
            })

        student_form = {
            "form": form,
            "student": student
        }
        forms.append(student_form)

    if request.method == 'POST':
        for form in forms:
            form_instance = form['form']
            student = Student.objects.get(id=form_instance.student_id)

        return HttpResponse("Attendance updated successfully!")
    context = {
        "forms":forms,
        'batch_id': batch_id,
        'session': session,
        'date': date,
    }
    return render(request, 'fill_theory_attendance.html', context)


def add_update_Theory_attendance(request, *args, **kwargs):
    if request.method == 'POST':
        batch_id = request.POST.get("batch_id")
        session = request.POST.get("session")
        student_id =request.POST.get('student_id') 
        date_str = request.POST.get("date")
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        student=Student.objects.get(id=student_id)
        batch = get_object_or_404(BatchModel, id=batch_id)
        try:
            attendance = BatchTheoryAttendance.objects.get(batch=batch,student=student,date=date,session=session)
            attendance.entry_time=request.POST.get('entry_time')
            attendance.exit_time=request.POST.get('exit_time')
            attendance.save()
            return redirect('theory_attendance_form',batch_id=batch_id,date=date_str,session=session)
        except BatchTheoryAttendance.DoesNotExist:
            attendnace = BatchTheoryAttendance.objects.create
            attendnace = BatchTheoryAttendance.objects.create(batch=batch,student=student,date=date,session=session,entry_time=request.POST.get('entry_time'),exit_time=request.POST.get('exit_time'))
            attendnace.save()
            return redirect('theory_attendance_form',batch_id=batch_id,date=date_str,session=session)
        
def delete_theory_attendance(request, *args, **kwargs):
    batch_id = kwargs.get("batch_id")
    session = kwargs.get("session")
    date_str = kwargs.get("date")
    date = datetime.strptime(date_str, "%Y-%m-%d").date()

    batch = get_object_or_404(BatchModel, id=batch_id)

    objects = BatchTheoryAttendance.objects.filter(batch=batch,session=session,date=date)
    objects.delete()
    return redirect('theory_attendance',pk=batch_id)

def daily_attendance_list(request):
    attendances = DailyAttendance.objects.all()
    return render(request, 'attendance_list.html', {'attendances': attendances})

def daily_attendance_create(request):
    if request.method == 'POST':
        form = DailyAttendanceForm(request.POST)
        if form.is_valid():
            try:
                attendance = form.save()
                return redirect('attendance_list')
            except :
                form.add_error('students', 'Attendance for this date already exists.')
    else:
        form = DailyAttendanceForm()
    return render(request, 'attendance_form.html', {'form': form})


def daily_attendance_update(request, pk):
    attendance = get_object_or_404(DailyAttendance, pk=pk)
    if request.method == 'POST':
        form = DailyAttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            attendance = form.save()
            return redirect('attendance_list')
    else:
        form = DailyAttendanceForm(instance=attendance)
    return render(request, 'attendance_form.html', {'form': form})

def daily_attendance_delete(request, pk):
    attendance = get_object_or_404(DailyAttendance, pk=pk)
    if request.method == 'POST':
        attendance.delete()
        return redirect('attendance_list')
    return render(request, 'attendance_confirm_delete.html', {'attendance': attendance})



def daily_staff_attendance_list(request):
    attendances = StaffDailyAttendance.objects.all()
    return render(request, 'staff_list.html', {'attendances': attendances})

def daily_staff_attendance_create(request):
    if request.method == 'POST':
        form = StaffDailyAttendanceForm(request.POST)
        if form.is_valid():
            try:
                attendance = form.save()
                return redirect('staff_attendance_list')
            except :
                form.add_error('staffs', 'Attendance for this date already exists.')
    else:
        form = StaffDailyAttendanceForm()
    return render(request, 'attendance_form.html', {'form': form})

def daily_staff_attendance_update(request, pk):
    attendance = get_object_or_404(StaffDailyAttendance, pk=pk)
    if request.method == 'POST':
        form = StaffDailyAttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            attendance = form.save()
            return redirect('staff_attendance_list')
    else:
        form = StaffDailyAttendanceForm(instance=attendance)
    return render(request, 'attendance_form.html', {'form': form})

def daily_staff_attendance_delete(request, pk):
    attendance = get_object_or_404(staffDailyAttendance, pk=pk)
    if request.method == 'POST':
        attendance.delete()
        return redirect('staff_attendance_list')
    return render(request, 'attendance_confirm_delete.html', {'attendance': attendance})



def dashboard(request):
    form = DashboardForm(request.GET or None)

    staff_id = request.GET.get('staff', Staff.objects.first().id if Staff.objects.exists() else None)
    date = request.GET.get('date', current_date)
    lab_attendance = request.GET.get('lab_attendance', 'lab')

    if not all([staff_id, date, lab_attendance]):
        raise Http404("Missing parameters in the URL")

    try:
        staff = Staff.objects.get(id=staff_id)
    except Staff.DoesNotExist:
        raise Http404("Staff does not exist")

    batches = BatchModel.objects.filter(batch_staff=staff)

    attendance_data = []

    for batch in batches:
        if lab_attendance == 'lab':
            summary = BatchLabAttendanceSummary(batch, date)
        else:
            summary = BatchTheoryAttendanceSummary(batch, date)

        attendance_summary = summary.get_attendance_summary()
        attendance_data.append(attendance_summary)

    context = {
        'attendance_data': attendance_data,
        'form':form,
    }

    return render(request, 'dashboard.html', context)


def router(request):
    return render(request,'router.html')