from django.urls import path
from . import views 

urlpatterns = [
    path('api/get/user-ticket/', views.ApiGetUserTicket, name='ApiGetUserTicket'),
]