from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms


from accounts.models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')
    class Meta:
        model = Account
        fields = (
            "email",
            "username",
            "password1",
            "password2",
        )


class AccountUpdateForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'username')

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" is already in use.' % email)

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" is already in use.' % username)

    def clean(self):
        if self.is_valid():
            password = self.cleaned_data['password']
            confirm_password = self.cleaned_data['confirm_password']
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match")


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid login')