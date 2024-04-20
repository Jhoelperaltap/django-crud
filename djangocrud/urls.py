
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name='home'), 
    path("signup/", views.signup, name='signup'),
    path("tasks/", views.tasks, name='tasks' ),
    path('tasks_complete/', views.tasks_complete, name='tasks_complete'),
    path("tasks/create/", views.create_task, name='create_task'),
    path('tasks/<int:task_pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_pk>/complete/', views.complete_task, name='complete_task'),
    path('tasks/<int:task_pk>/delete/', views.delete_task, name='delete_task'),
    path("logout/", views.logoutuser, name='logout'),
    path("signin/", views.signin, name='signin'),
    
]
