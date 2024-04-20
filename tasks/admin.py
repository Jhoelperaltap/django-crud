from django.contrib import admin
from .models import Task 

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    
""""
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'complete', 'created', 'datecompleted', 'important', 'user']
    search_fields = ['title', 'description']
    list_filter = ['complete', 'important', 'datecompleted']
"""
admin.site.register(Task, TaskAdmin)