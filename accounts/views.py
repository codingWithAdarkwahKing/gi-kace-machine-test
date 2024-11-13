import hashlib
import secrets

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.signing import TimestampSigner, SignatureExpired, Signer
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.crypto import salted_hmac, get_random_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from accounts.models import EmailConfirmation
from .forms import RegistrationForm, AccountAuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect

# @csrf_protect
# def signup_view(request):
#     if request.user.is_authenticated:
#         return redirect('task_management:home')
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             email = form.cleaned_data.get('email')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(email=email, password=raw_password)
#             login(request, user)
#             return redirect('task_management:home')
#     else:
#         form = RegistrationForm()
#     return render(request, 'accounts/signup.html', {'form': form})

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('task_management:home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.email_confirmed = False
            user.save()

            print(user.pk)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token_encoded = default_token_generator.make_token(user)
            confirm_url = reverse('accounts:confirm_email', kwargs={'uidb64': uidb64, 'token': token_encoded})

            email_confirmation = EmailConfirmation.objects.create(user=user, new_email=user.email, token=token_encoded, uid=user.pk)
            email_confirmation.save()

            current_site = get_current_site(request)
            subject = 'Confirm Registration'
            message = render_to_string('accounts/registration_confirmation.html', {
                'user': user,
                'confirm_url': confirm_url,
                'domain': current_site.domain,
            })
            plain_message = strip_tags(message)
            from_email = 'adarkwahking4@gmail.com'
            recipient_list = [user.email]

            send_mail(subject, plain_message, from_email, recipient_list, html_message=message)

            return redirect('accounts:verification_pending')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/signup.html', {'form': form})


def verification_pending(request):
    return render(request, 'accounts/verification_pending.html')


User = get_user_model()


def confirm_email(request, uidb64, token):
    user = None
    try:
        uid = (urlsafe_base64_decode(uidb64)).decode()
        print(f"UID: {uid}")
        print(f"Token in URL: {token}")
        email_confirmation = EmailConfirmation.objects.get(uid=uid)
        print(f"Token in DB: {email_confirmation.token}")

        if default_token_generator.check_token(email_confirmation.user, token):
            email_confirmation.email_confirmed = True
            email_confirmation.save()

            user = email_confirmation.user
            user.is_active = True
            user.email_confirmed = True
            user.save()
            login(request, user)

            return render(request, 'accounts/email_confirmation_success.html')
    except (TypeError, ValueError,):
        if user is not None:
            user.delete()

    return render(request, 'accounts/email_confirmation_error.html')
# ############### Account signup handling ########################



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