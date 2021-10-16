import django
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.contrib.auth import login

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard')
    else:
        return render(request, 'pages/index.html')

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'pages/dashboard.html', {'name': request.user.get_username()})
    else:
        return HttpResponseRedirect('/accounts/login')

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    errors = []
    if request.method == 'POST':
        if request.POST['name'] == '' or request.POST['password'] == '':
            errors.append('Please fill required fileds')
            return render(request, 'registration/register.html', {'errors': errors})
        if len(request.POST['password']) < 6:
            if 'Please fill required fileds' not in errors: errors.append('Password must be at least 6 charachters long')
            return render(request, 'registration/register.html', {'errors': errors})
        if request.POST['password'] != request.POST['confpassword']:
            if 'Please fill required fileds' not in errors: errors.append('Passwords didn\'t match')
            return render(request, 'registration/register.html', {'errors': errors})

        else:
            try:
                user = User.objects.create_user(request.POST['name'], request.POST['email'], request.POST['password'])
                user.save()
                return HttpResponseRedirect('/accounts/login')
            except django.db.IntegrityError:
                errors.append('User already exists')
                return render(request, 'registration/register.html', {'errors': errors})
    else:
        return render(request, 'registration/register.html')
