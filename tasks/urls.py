from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('users-view/', views.UsersView.as_view(), name='users_view'),
    path('create-user/', views.CreateUser.as_view(), name='create_user'),
    path('edit-user/<int:pk>', views.CreateUser.as_view(), name='edit_user'),
    path('assign-user/', views.SubordinateAssignForm.as_view(), name='assign_user'),
    path('delete-user/<int:pk>', views.delete_user, name='delete_user'),

    path('view-task/', views.TaskView.as_view(), name='view_task'),
    path('create-task/', views.TaskCreateView.as_view(), name='create_task'),
    path('edit-task/<int:pk>', views.TaskCreateView.as_view(), name='edit_task'),
    path('complete-task/<int:pk>', views.TaskComplete.as_view(), name='complete_task'),
    path('delete-task/<int:pk>', views.delete_task, name='delete_task'),

]