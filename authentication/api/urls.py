from django.urls import path
from knox import views as knox_views
from authentication.api.views import LoginView, LogoutView, ProfileView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # Optional: Knox provides a logout-all endpoint
    path('logout-all/', knox_views.LogoutAllView.as_view(), name='logout_all'),
]
