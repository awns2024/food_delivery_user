from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
urlpatterns = [
  
     path('login/', UserLoginView.as_view(), name = 'user login'),
     path('update/<uuid:input>/', UserUpdateView.as_view(), name = 'user update'),
     path('delete/', UserDeleteView.as_view(), name = 'user delete'),
]
