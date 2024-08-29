from django.urls import path, include
from .views import UserDetail, signup, base, login_view, logout_view

urlpatterns = [
    path('', base, name='base'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/<int:pk>/', UserDetail.as_view(), name='profile'),
]