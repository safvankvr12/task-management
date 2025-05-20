from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from tasks.models import Subordinates, Tasks
from .forms import AssignUsers, CompletedForm, TaskForm, RegisterForm, UserForm


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request) 
    return redirect('login') 


class UsersView(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'users.html', {'users': users})

class CreateUser(LoginRequiredMixin,View):
    def get(self, request, pk=None):
        if pk:
            instance = User.objects.filter( pk=pk).first()
        else:
            instance = None
        form = UserForm(instance=instance)
        return render(request, 'create_user.html', {'form': form})
    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users_view')
        return render(request, 'create_user.html', {'form': form})

def delete_user(request, pk):
    sub_user = request.user
    user = User.objects.filter(id=pk).first()
    if sub_user.is_superuser or user in sub_user.subordinate_user.assignees.all():
        user.delete()
    return redirect("users_view")


class SubordinateAssignForm(LoginRequiredMixin, View):
    def get(self, request):
        form = AssignUsers(req=request)
        return render(request, 'assign_user.html', {'form': form})
    
    def post(self, request):
        form = AssignUsers(request.POST)
        if 'user' in form.errors:
            form.errors.pop('user')
        if form.is_valid():
            user = form.data.get('user')
            assignees = form.data.getlist('assignees')

            sub, created = Subordinates.objects.get_or_create(user=user)

            sub.assignees.set(assignees)
            sub.save()

            return redirect("users_view")

        return render(request, 'assign_user.html', {'form': form})


class TaskView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser:
            tasks = Tasks.objects.all()
        else:
            try:
                tasks = (
                    Tasks.objects.filter(assigned_to__in=request.user.subordinate_user.assignees.all()) |
                    Tasks.objects.filter(assigned_to=request.user)
                )
            except:
                tasks = Tasks.objects.filter(assigned_to=request.user)
        return render(request, 'tasks.html', {'tasks': tasks})


class TaskCreateView(LoginRequiredMixin, View):
    def get(self, request,pk=None):
        if pk:
            instance = Tasks.objects.filter( pk=pk).first()
        else:
            instance = None
        form = TaskForm(instance=instance, req=request)
        return render(request, 'task_create.html', {'form': form})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_task')
        return render(request, 'task_create.html', {'form': form})

class TaskComplete(LoginRequiredMixin, View):
    def get(self, request, pk):
        instance = Tasks.objects.get(pk=pk)
        form = CompletedForm(instance=instance)
        return render(request, 'task_complete.html', {'form': form})
    
    def post(self, request, pk):
        task = Tasks.objects.get(pk=pk)
        form = CompletedForm(request.POST, instance=task)
        if form.is_valid():
            task.status = "completed"
            task.completion_report = form.data.get("completion_report")
            task.worked_hours = form.data.get("worked_hours")
            task.save()
            return redirect('view_task')
        return render(request, 'task_complete.html', {'form': form})


def delete_task(request, pk):
    sub_user = request.user
    task = Tasks.objects.filter(id=pk).first()
    if sub_user.is_superuser or task.assigned_to in sub_user.subordinate_user.assignees.all():
        task.delete()
    return redirect("view_task")

