from django import forms
from django.forms import TimeInput
from .models import BatchLabAttendance,BatchTheoryAttendance,DailyAttendance,StaffDailyAttendance
from apps.staffs.models import Staff
import datetime

class BatchLabAttendanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['entry_time'].widget = TimeInput(attrs={'type': 'time'})
        self.fields['exit_time'].widget = TimeInput(attrs={'type': 'time'})
    student_id = forms.IntegerField(widget=forms.HiddenInput())
    batch_id = forms.IntegerField(widget=forms.HiddenInput())
    session = forms.CharField(max_length=100, widget=forms.HiddenInput())
    date = forms.DateField(widget=forms.HiddenInput())

    class Meta:
        model = BatchLabAttendance
        fields = ['entry_time', 'exit_time']
    

class BatchTheoryAttendanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['entry_time'].widget = TimeInput(attrs={'type': 'time'})
        self.fields['exit_time'].widget = TimeInput(attrs={'type': 'time'})
    student_id = forms.IntegerField(widget=forms.HiddenInput())
    batch_id = forms.IntegerField(widget=forms.HiddenInput())
    session = forms.CharField(max_length=100, widget=forms.HiddenInput())
    date = forms.DateField(widget=forms.HiddenInput())

    class Meta:
        model = BatchTheoryAttendance
        fields = ['entry_time', 'exit_time']
    
class DailyAttendanceForm(forms.ModelForm):
    class Meta:
        model = DailyAttendance
        fields = ['students']
        widgets = {
            'students': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude 'date' field from the form
        self.fields.pop('date', None)
        self.fields['students'].required=False


class StaffDailyAttendanceForm(forms.ModelForm):
    class Meta:
        model = StaffDailyAttendance
        fields = ['staffs']
        widgets = {
            'staffs': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude 'date' field from the form
        self.fields.pop('date', None)
        self.fields['staffs'].required=False


'''
    staff = forms.ModelChoiceField(queryset=Staff.objects.all(), empty_label="Select Staff")
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    lab_or_theory = forms.ChoiceField(choices=[('lab', 'Lab'), ('theory', 'Theory')], widget=forms.RadioSelect)
'''
class DashboardForm(forms.Form):
    staff = forms.ModelChoiceField(queryset=Staff.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    lab_attendance = forms.ChoiceField(choices=[('lab', 'Lab'), ('theory', 'Theory')], widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
    def __init__(self, *args, **kwargs):
        super(DashboardForm, self).__init__(*args, **kwargs)
        
        # Set the initial value for staff field
        first_staff = Staff.objects.first()
        if first_staff:
            self.fields['staff'].initial = first_staff
        
        # Set the initial value for date field as current date
        self.fields['date'].initial = datetime.date.today()