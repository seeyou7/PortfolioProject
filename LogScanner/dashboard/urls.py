from django.urls import path
from .views import dashboard
from .views import app_logs_view
from .views import auth_logs_view
from .views import network_logs_view
#from .views import test_log_path

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('app-logs/', app_logs_view, name='app_logs'),
    path('auth-logs/', auth_logs_view, name='auth_logs'),
    path('network-logs/', network_logs_view, name='network_logs'),
    #path('test-log-path/', test_log_path, name='test-log-path'),
]