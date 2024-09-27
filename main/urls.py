from django.urls import path, include
from .views import (signup, user_detail, update_profile, 
                    avatar_view, UpdatesListView, UpdatesDetailView,
                    update_create, login_view, logout_view)

urlpatterns = [
    path('', UpdatesListView.as_view(), name='updates'),
    path('update/add/', update_create, name='update_create'),
    path('update/<int:pk>/', UpdatesDetailView.as_view(), name='update_create'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/<int:pk>/', user_detail, name='profile'),
    path('profile/<int:pk>/edit/', update_profile, name='update_profile'),
    path('media/avatars/<str:filename>', avatar_view),
]