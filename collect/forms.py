import email
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post,ReviewRating,Rating
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
  email = forms.EmailField()

  class Meta:
    model = User
    fields = ['username','email','password1','password2']

  def save(self, commit=True):
    user = super(NewUserForm, self).save(commit=False)
    user.email = self.cleaned_data['email']
    if commit:
      user.save()
    return user


class EventAttendForm(forms.Form):
    name = forms.CharField(label='Full names',max_length=100)
    email = forms.EmailField(label='Email')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['weight']
class postProjectForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ['title','description','photo']