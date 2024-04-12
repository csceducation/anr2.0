from django import forms

class DateForm(forms.Form):
    date = forms.DateField(label="Select Date", widget=forms.DateInput(attrs={'type': 'date'}))
    content = forms.CharField(
        required=False,
        label='Content',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
    )