from django.urls import path
from . import views

app_name = 'log_user'

urlpatterns = [
    # path('', views.index, name='index'),
    path('/<str:type>', views.index, name='index'),
    path('/get_log/<str:type>', views.get_log, name='get_log'),
    
]