from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import checklist
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.
@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
         task = request.POST.get('task')
         new_checklist = checklist(user=request.user, checklist_name=task)
         new_checklist.save()

    if request.user.is_authenticated:
        all_checklists = checklist.objects.filter(user=request.user)
        
         if request.headers.get('Content-Type') == 'application/json':
                checklist_data = list(all_checklists.values())
                return JsonResponse(checklist_data, safe=False)
             
        context = {
            'checklists': all_checklists
        }
        return render(request, 'alistapp/todo.html', context)
    else:      
        return redirect('login')
    #all_checklists = checklist.objects.filter(user=request.user)
    #context = {
    #     'checklists' : all_checklists
    #}
    #return render(request, 'alistapp/todo.html', context)
   
    
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 3:
            messages.error(request, 'Password is too short')
            return redirect('register')
        
        get_all_users_by_username = User.objects.filter(username=username)
        if get_all_users_by_username:
            messages.error(request, 'Username already exists')
            return redirect('register')
        
        new_user = User.objects.create_user(username=username, email=email, password=password)
        
        new_user.save()
        messages.success(request, 'User successfully created, login now')
        return redirect('login')
    
    return render(request, 'alistapp/register.html', {})

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        
        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
                login(request, validate_user)
                return redirect('home-page')
        else:
                messages.error(request, 'Error user does not exist')
                return redirect('login')
    return render(request, 'alistapp/login.html', {})

def DeleteTask(request, name):
     get_checklist = checklist.objects.get(user=request.user, checklist_name=name)
     get_checklist.delete()
     return redirect('home-page')

def Update(request, name):
     pass
