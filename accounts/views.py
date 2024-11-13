from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm, AccountAuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('task_management:home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('task_management:home')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/signup.html', {'form': form})

@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        return redirect('task_management:home')
    
    if request.method == 'POST':
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('task_management:home') 
    else:
        form = AccountAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('task_management:home')


def must_authenticate(request):
    return render(request, 'accounts/must_authenticate.html', {})


@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Your account has been deleted.')
        logout(request)
        return redirect('task_management:home')

    return render(request, 'accounts/delete_account.html')