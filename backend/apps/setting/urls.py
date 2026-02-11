from django.urls import path
from . import views

urlpatterns = [
    path('api/setting/get/column-audio-record/', views.ApiGetColumnAudioRecord, name='ApiGetColumnAudioRecord'),
    path('api/setting/save/column-audio-record/', views.ApiSaveColumnAudioRecord, name='ApiSaveColumnAudioRecord'),
]