from django.urls import path
from . import views 
from apps.user_permissions.views import UserGroupAPIView

app_name = 'user_permissions'

urlpatterns = [
    path('', views.index, name='index'),
    path('/add', views.user_add, name='user_add'),
    path('/user-management/create', views.create, name='user-permissions-create'),
    path('/user-group', UserGroupAPIView.as_view(), name='user-group'),
    path('/user-team', views.user_team, name='user-team'),
    path('/edit/<int:user_id>/', views.user_edit, name='user_edit'),
    path('/get-team-maindatabase/', views.get_team_maindatabase, name="get_team_maindatabase"),
    path('/delete/<int:user_id>/', views.delete_user_permission, name='delete_user_permission'),
    path('/get-all-roles-permissions/', views.get_all_roles_permissions, name='get_all_roles_permissions'),
    path('/check-username/', views.check_username, name='check_username'),
    path('/user-management/update/<int:user_id>/', views.update_user, name='user-permissions-update'),
    path('/change-status/<int:user_id>/', views.change_user_status, name='change_user_status'),
    
    
]