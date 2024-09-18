from django.urls import path

from .views import groups, group, group_add, group_edit, group_delete

urlpatterns=[
    path('', groups, name='groups'),
    path('add/', group_add, name='group_add'),
    path('<slug:slug>/', group, name='group'),
    path('<slug:slug>/edit', group_edit, name='group_edit'),
    path('<slug:slug>/delete', group_delete, name='group_delete'),
]