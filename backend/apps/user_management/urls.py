from django.urls import path
from . import views 

urlpatterns = [
    path('api/user-management/index/', views.ApiIndexUserManagement, name='ApiIndexUserManagement'),
    path('api/user-management/change-status/<int:user_id>/', views.ApiChangeUserStatus, name='ApiChangeUserStatus'),
    
]