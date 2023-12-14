from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

# Show all tasks that have been created
@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {
        'tasks': tasks 
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required
def create_task(request):
    if request.method == 'GET': 
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:         
        task = Task.objects.create(
            title = request.POST['title'], 
            description = request.POST['description'], 
            important = 'important' in request.POST,
            user = request.user
        )

        return redirect('tasks')

# Update a task
@login_required
def task_detail(request, task_id):
    if request.method == 'GET': 
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        task = get_object_or_404(Task, pk=task_id)
        form = TaskForm(request.POST, instance=task)
        form.save()
        return redirect('tasks')

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
    else:
        return redirect('tasks')
    
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    else:
        return redirect('tasks')

# Create an user
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form' : UserCreationForm
        })
    else:       
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                # login - Function that creates a unique id in the developer tools. 
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'msg': 'User already exists'
                })        
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'msg': 'Password do not match'
        })
    

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
        'form': AuthenticationForm
    })    
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('tasks')
        else:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'msg': 'Username or password is incorrect'
            })
        

# Function that logs you out
@login_required
def log_out(request):
    logout(request)
    return redirect('home')