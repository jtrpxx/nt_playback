from django.urls import path
from . import views

app_name = 'configuration'

urlpatterns = [
    path("/audio-search",views.index_audio_search,name="config-audio-search"),
    path("/group", views.index_group, name="config-group"),
    path("/group/add", views.create_form_group, name="form-group-add"),
    path("/team", views.index_team, name="config-team"),
    path("/team/add", views.create_form_team, name="config-team-add"),
    
    path("/create-config-group", views.create_config_group, name="create-config-group"),
    path("/create-config-team", views.create_config_team, name="create-config-team"),
    path("/group/details", views.get_group_details, name="get-group-details"),
    path("/group/update", views.update_config_group, name="update-config-group"),
    path("/group/delete", views.delete_config_group, name="delete-config-group"),
    path("/team/get-by-group", views.get_teams_by_group, name="get-teams-by-group"),
    path("/group/list", views.get_group_list, name="get-group-list"),
    
    path("/team/details", views.get_team_details, name="get-team-details"),
    path("/team/update", views.update_config_team, name="update-config-team"),
    path("/team/delete", views.delete_config_team, name="delete-config-team"),
    path("/role", views.index_role, name="config-group"),
    path("/role/get-details/", views.get_role_details, name="get-role-details"),
    path("/role/create/", views.create_role, name="create"),
    path("/role/update/", views.update_role, name="update"),
    path("/role/delete/", views.delete_role, name="delete"),
]