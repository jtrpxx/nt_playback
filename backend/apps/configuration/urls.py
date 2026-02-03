from django.urls import path
from . import views
from apps.configuration.views import MainDatabaseAPIView

urlpatterns = [
    path("api/role/index/", views.ApiIndexRole, name="ApiIndexRole"),
    path("api/role/get-details/<int:role_id>/", views.ApiGetRoleDetails, name="ApiGetRoleDetails"),
    path("api/group/index/", views.ApiIndexGroup, name="ApiIndexGroup"),
    path("api/group/get/team-by-group/<int:group_id>/", views.ApiGetTeamByGroup, name="ApiGetTeamByGroup"),
    path("api/role/check/role-name/", views.ApiCheckRoleName, name="ApiCheckRoleName"),
    path("api/get/database/", MainDatabaseAPIView.as_view(), name="ApiGetDatabase"),
    path("api/role/create/", views.ApiCreateRole, name="ApiCreateRole"),
    path("api/role/edit/<int:role_id>/", views.ApiCreateRole, name="ApiUpdateRole"),
    path("api/role/delete/<int:role_id>/", views.ApiDeleteRole, name="ApiDeleteRole"),
]