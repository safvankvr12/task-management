# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Subordinates, Tasks

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'email', 'first_name', 'last_name')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'email', 'first_name', 'last_name','is_superuser', 'is_staff']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        if cleaned_data.get('is_superuser'):
            cleaned_data['is_staff'] = True
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class AssignUsers(forms.ModelForm):
    class Meta:
        model = Subordinates
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        req = kwargs.pop('req', None) 
        super().__init__(*args, **kwargs)
        
        if req:
            if req.user.is_superuser:
                self.fields['user'].queryset = User.objects.filter(is_staff=True)
            elif req.user.is_staff:
                self.fields['user'].queryset = User.objects.filter(is_staff=True, is_superuser=False)


class TaskForm(forms.ModelForm):
    due_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    class Meta:
        model = Tasks
        fields='__all__'
        exclude = ['completion_report', 'worked_hours', 'status']
    
    def __init__(self, *args, **kwargs):
        req = kwargs.pop('req', None) 
        super().__init__(*args, **kwargs)
        if req:
            if req.user.is_superuser:
                self.fields['assigned_to'].queryset = User.objects.all()
            elif req.user.is_staff:
                self.fields['assigned_to'].queryset = User.objects.exclude(is_superuser=True)


class CompletedForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ["completion_report", "worked_hours"]