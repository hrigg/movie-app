from django.urls import path
from . import views


urlpatterns = [
    path('', views.MovieList.as_view(), name='movie_list'),
    path('movies/', views.Home.as_view(), name= 'movie_list'),
    path('movies/new', views.MovieCreate.as_view(), name='movie_create'), 
    path('movies/<int:pk>', views.MovieDetail.as_view(), name='movie_detail'),
    path('movies/<int:pk>/update', views.MovieUpdate.as_view(), name='movie_update'),
    path('movies/<int:pk>/delete', views.MovieDelete.as_view(), name='movie_delete'),
    path('movies/<int:pk>/review/new/', views.ReviewCreate.as_view(), name='review_create'),
    path('list/<int:pk>/movies/<int:movie_pk>/', views.ListMovieAssoc.as_view(), name="list_movie_assoc"),
    path('list/<int:pk>', views.ListDetail.as_view(), name="list_detail"),
    path('list/new', views.ListCreate.as_view(), name='list'),
    path('accounts/signup/', views.Signup.as_view(), name="signup")
]