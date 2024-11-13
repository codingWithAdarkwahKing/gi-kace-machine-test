from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        if not password:
            raise ValueError('The Password field must be set')

        email = self.normalize_email(email)

        if self.model.objects.filter(email=email).exists():
            raise ValidationError('An account with this email address already exists.')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The Password field must be set')
        if not username:
            raise ValueError('The Username field must be set')

        email = self.normalize_email(email)
        user = self.create_user(email, username, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_superuser


User = get_user_model()


class EmailChangeRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    new_email = models.EmailField()
    token = models.CharField(max_length=100, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Email Change Request for {self.user.email} to {self.new_email}"


class EmailConfirmation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    new_email = models.EmailField()
    token = models.CharField(max_length=100, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    email_confirmed = models.BooleanField(default=False)
    uid = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Confirmation for {self.user.username}"