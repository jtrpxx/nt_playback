from django.urls import path
from . import views

urlpatterns = [
	path('api/audio/list/', views.ApiGetAudioList, name='ApiGetAudioList'),
	path('api/home/index/', views.ApiIndexHome, name='ApiIndexHome'),
]

