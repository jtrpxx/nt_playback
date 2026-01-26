from django.urls import path
from . import views

urlpatterns = [
    path("api/role/index/", views.ApiIndexRole, name="ApiIndexRole"),
    path("api/role/get-details/<int:role_id>/", views.ApiGetRoleDetails, name="ApiGetRoleDetails"),
    # path("api/role/create/", views.ApiCreateRole, name="ApiCreateRole"),
    # path("api/role/update/", views.ApiUpdateRole, name="ApiUpdateRole"),
    # path("api/role/delete/", views.ApiDeleteRole, name="ApiDeleteRole"),
]