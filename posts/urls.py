# apps/posts/urls.py
from django.urls import path
from .views import (
    PostListCreateView, PostRetrieveUpdateDestroyView,
    FollowListCreateView, UnfollowDestroyView,
    LikeCreateDestroyView,
    CommentListCreateView,
    AllUserPostView,
)

urlpatterns = [
    # Post URLs
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),  # список всех постов / создание поста
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),  # просмотр / редактирование / удаление поста
    path('all/post/',AllUserPostView.as_view(),name='all-post'),

    # Follow URLs
    path('follow/', FollowListCreateView.as_view(), name='follow-list-create'),  # список подписок и подписка на пользователя
    path('unfollow/<int:following_id>/', UnfollowDestroyView.as_view(), name='unfollow'),  # отписка от пользователя

    # Like URLs
    path('posts/<int:post_id>/like/', LikeCreateDestroyView.as_view(), name='like-post'),  # поставить/снять лайк
 
    # Comment URLs
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='post-comments'),  # список комментариев / создание комментария
]
