from django.urls import path
from .views import *
urlpatterns = [
  
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),  # список всех постов / создание поста
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),  # просмотр / редактирование / удаление поста
    path('all/post/',AllUserPostView.as_view(),name='all-post'),
]
