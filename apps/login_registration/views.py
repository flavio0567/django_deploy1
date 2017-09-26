from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
    return render(request, 'login_registration/index.html')

def login(request):
    return render(request, 'login_registration/login.html')

def check_login(request):
    context = User.objects.login_validator(request.POST)
    errors = context['errors']
    if len(errors):
        for tag, error in errors.iteritems():
            print error
            messages.error(request, error, extra_tags=tag)
        return render(request, 'login_registration/login.html')
    else:
        request.session['name'] = context['user']
        return render(request, 'login_registration/result.html' )

def register(request):
    return render(request, 'login_registration/register.html')

def check_register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags = tag)
        return render(request, 'login_registration/register.html')
    else:
        hashed = bcrypt.hashpw((request.POST['passwd1'].encode()), bcrypt.gensalt(5))
        User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email1'],
            password=hashed
        )
        request.session['name'] = User.objects.last().first_name

    return render(request, 'login_registration/result.html' )
#
