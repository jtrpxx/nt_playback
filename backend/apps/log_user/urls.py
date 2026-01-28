from django.urls import path
from . import views

urlpatterns = [
    path('/api/log-user/get-log/<str:type>', views.ApiGetUserLogs, name='ApiGetUserLogs'),
    
]