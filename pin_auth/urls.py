from django.urls import path
from .views import RegisterView, LoginView, HomeView, LogoutView, ShoulderSurfingProtectionView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', LoginView.as_view()), 
    path('protection-settings/', ShoulderSurfingProtectionView.as_view(), name='protection_settings'),
]