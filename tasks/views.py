
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request,'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request,'signup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
               user = User.objects.create_user(username=request.POST['username'],
                                               password=request.POST['password1'])
               user.save()
               login(request, user)
               return redirect('tasks')
            except IntegrityError:
               return render(request,'signup.html', {'form': UserCreationForm, 
                                                     'error': 'Username is already taken'})
       
        return render(request,'signup.html', {'form': UserCreationForm, 
                                             'error': 'Passwords did not match'})
@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request,'tasks.html', {'tasks': tasks}) 

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
            })
    else:
        try:
            form = TaskForm(request.POST)
            newtask = form.save(commit=False)
            newtask.user = request.user
            newtask.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {'form': TaskForm, 
                                                        'error': 'Bad data passed in. Try again.'})

@login_required
def task_detail(request, task_pk):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_pk, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    
    else:
        task = get_object_or_404(Task, pk=task_pk, user=request.user)
        try:
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 
                                                        'error': 'Bad info passed in. Try again.'})

@login_required
def complete_task(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
 
@login_required   
def delete_task(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')    
 
@login_required    
def tasks_complete(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def logoutuser(request):
    logout(request)
    return redirect('home')




def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm()})
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('tasks')

        return render(request, 'signin.html', {'form': form, 'error': 'Username and password did not match'})













 
""""
def signin(request):
    if request.method == 'GET':
        return render(request,'signin.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], 
                            password=request.POST['password']) 

        if user is not None:
            return render(request, 'signin.html',
                          {'form': AuthenticationForm, 
                           'error': 'Username and password did not match'})
      
        else:
            login(request, user)
            return redirect('tasks')
           """