from django.urls import path
from . import views

urlpatterns = [
    # Example route
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
]
