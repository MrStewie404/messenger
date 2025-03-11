from django.urls import path, include
from .views import *

urlpatterns = [
    path('', base),
    path('modules/', module_search, name='modules'),
    path('modules/create/', modules_create, name='modules_create'),
    path('modules/add/<int:pk>/', modules_add, name='modules_add'),
    path('modules/del/<int:pk>/', modules_del, name='modules_del'),
    path('modules/upd/<int:pk>/', modules_upd, name='modules_upd'),
    path('updates/', UpdatesListView.as_view(), name='updates'),
    path('update/add/', update_create, name='update_create'),
    path('update/upd/<int:pk>', update_update, name='update_update'),
    path('update/del/<int:pk>', update_delete, name='update_delete'),
    path('update/<int:pk>/', UpdatesDetailView.as_view(), name='update'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/<int:pk>/', user_detail, name='profile'),
    path('profile/<int:pk>/edit/', update_profile, name='update_profile'),
    path('media/avatars/<str:filename>', avatar_view),
    path('modules/upd_seq/', module_update_sequence),
]