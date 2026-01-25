from django.urls import path
from . import views

urlpatterns = [
	path('api/audio/list/', views.ApiGetAudioList, name='api_get_audio_list'),
	path('api/home/index/', views.ApiIndexHome, name='api_index_home'),
]

