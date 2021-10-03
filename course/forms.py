from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Course, Module
from django.forms.models import inlineformset_factory
from django.forms.models import BaseModelFormSet
from django.forms.formsets import DELETION_FIELD_NAME
User = get_user_model()


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'validate', 'id': 'eamil'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'validate',
            'id': 'password',
        }
))

class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('subject',
                  'title',
                  'slug',
                  'overview',
                  'cover')
        widgets = {
            'subject': forms.Select(),
            'title': forms.TextInput(attrs={'class': 'validate'}),
            'slug': forms.TextInput(attrs={'class': 'validate'}),
            'overview': forms.Textarea(attrs={'class': 'validate'}),
        }

# class FormSet(BaseModelFormSet):
#     def add_fields(self, form, index):
#         super(FormSet, self).add_fields(form, index)
#         form.fields[DELETION_FIELD_NAME].label = 'checkbox'

ModuleFormSet =inlineformset_factory(Course,
                                     Module,
                                     fields=['title',
                                             'description',
                                             'image',
                                             'file',
                                             'video'],
                                     extra=2,
                                     can_delete=False)

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'age',
                  'phone_number',
                  'bio',
                  'picture',)
