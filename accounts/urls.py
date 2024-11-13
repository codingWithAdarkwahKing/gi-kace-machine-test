from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.signup_view, name='signup'),
    path('accounts/signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('must-authenticate/', views.must_authenticate, name='must_authenticate'),
    path('accounts/login/', views.login_view, name='login'),
    path('delete_account/', views.delete_account, name='delete_account'),
]