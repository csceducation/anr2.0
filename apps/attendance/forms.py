from django import forms

class DateForm(forms.Form):
    date = forms.DateField(label="Select Date", widget=forms.DateInput(attrs={'type': 'date'}))
