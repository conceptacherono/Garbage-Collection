import email
from django import forms
class EventAttendForm(forms.Form):
    name = forms.CharField(label='Full names',max_length=100)
    email = forms.EmailField(label='Email')