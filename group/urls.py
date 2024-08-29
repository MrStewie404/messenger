from django.urls import path

from .views import groups, group

urlpatterns=[
    path('', groups, name='groups'),
    path('<slug:slug>/', group, name='group')
]