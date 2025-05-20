from django.contrib import admin

from tasks.models import Tasks, Subordinates

# Register your models here.
admin.site.register(Tasks)
admin.site.register(Subordinates)