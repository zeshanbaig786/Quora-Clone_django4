from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from django.forms import BaseFormSet, formset_factory
from bootstrap5.widgets import RadioSelectButtonGroup
from django.contrib.auth.models import User
from .models import Profile,Question,Answer
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=101)
    last_name = forms.CharField(max_length=101)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ['question','description']

class AnswerForm(forms.ModelForm):
    
    class Meta:
        model = Answer
        fields = ['answer']


