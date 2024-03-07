from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register
from . import views


urlpatterns = [
    path('register/', register, name='register'),  #  registration
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),  # Built-in login view
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Built-in logout view
     
]
 