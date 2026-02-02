from django.urls import path
from . import views

urlpatterns = [
	path('api/audio/list/', views.ApiGetAudioList, name='ApiGetAudioList'),
	path('api/home/index/', views.ApiIndexHome, name='ApiIndexHome'),
	path('api/home/index/', views.ApiIndexHome, name='ApiIndexHome'),
	path('api/home/add/my-favorite-search/', views.ApiCreateMyFavoriteSearch, name='ApiAddMyFavoriteSearch'),
	path('api/home/check/my-favorite-search/', views.ApiCheckMyFavoriteName, name='ApiCheckMyFavoriteName'),
	path('api/home/edit/my-favorite-search/<int:myfavoriteId>/', views.ApiIndexHome, name='ApiEditMyFavoriteSearch'),
 
]

