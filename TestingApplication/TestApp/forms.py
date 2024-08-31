from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Test, Question, Answer


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'answer_options', 'right_answers', 'size_of_answers']
        widgets = {
            'answer_options': forms.CheckboxSelectMultiple(),
            'right_answers': forms.CheckboxSelectMultiple(),
        }


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['name', 'questions', 'size_of_pages', 'is_active']
        widgets = {
            'questions': forms.CheckboxSelectMultiple(),
        }


class UserRegistrationForm(UserCreationForm):
    # email = forms.EmailField(required=True)
    usable_password = None

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
