from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

@login_required
def home(request):
    search_input = request.GET.get('search') or ''
    date_input = request.GET.get('date_filter') or ''
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.info(request,"New task added!")
            return redirect('home')
    else:
        form = TaskForm()
    tasks = Task.objects.filter(user=request.user)

    if search_input:
        tasks = tasks.filter(title__icontains=search_input)

    if date_input:
        tasks = tasks.filter(created_at__date=date_input)

    return render(request, 'core/home.html', {'tasks':tasks.order_by('-created_at'), 'form':form, 'search_input':search_input, 'date_input':date_input})
    # return HttpResponse("<h1>Hello! World</h1>")

def is_manager(user):
    return user.groups.filter(name='Manager').exits()

@user_passes_test(is_manager)
def delete_task(request,item_id):
    task = get_object_or_404(Task, id=item_id)
    task.delete()
    return redirect('home')

def toggle_task(request,item_id):
    task = get_object_or_404(Task,id=item_id)
    task.is_completed = not task.is_completed
    task.save()
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,"Registration successful. Welcome!")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form':form})
