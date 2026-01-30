from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from .views import RegisterView, LogoutView, MeProfileView, UserProfileView , MeUpdateView ,AllUserProfileView ,ProfileUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('me/', MeProfileView.as_view()),
    path('me/update/', MeUpdateView.as_view()),
    path('users/<int:pk>/', UserProfileView.as_view()),
    path('all/users/',AllUserProfileView.as_view()),
    path('profile/update/', ProfileUpdateView.as_view()),


]
