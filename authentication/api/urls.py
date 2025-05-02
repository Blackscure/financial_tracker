from django.urls import path

from authentication.api.views import LoginView, LogoutView, ProfileView, RegisterView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # Fixed typo
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]