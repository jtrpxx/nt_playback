from django.urls import path
from . import views 

urlpatterns = [
    path('api/get/user/', views.ApiGetUser, name='ApiGetUser'),
    path('api/user-management/change-status/<int:user_id>/', views.ApiChangeUserStatus, name='ApiChangeUserStatus'),
    
]