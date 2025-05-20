from django.db import models
from django.contrib.auth.models import User


class Tasks(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed' )
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_tasks"
    )
    due_date = models.DateField()
    status = models.CharField(choices=STATUS_CHOICES, default="pending")
    completion_report = models.TextField(blank=True, null=True)
    worked_hours = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Tasks"
    
    def __str__(self) -> str:
        return self.title
    
class Subordinates(models.Model):
    user = models.OneToOneField(User, related_name = 'subordinate_user', on_delete=models.CASCADE)
    assignees = models.ManyToManyField(User)

    def __str__(self) -> str:
        return self.user.get_full_name()