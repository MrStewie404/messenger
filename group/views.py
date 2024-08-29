from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Group

@login_required
def groups(request):
    groups = Group.objects.all()
    return render(request, 'groups.html', {'groups': groups})

@login_required
def group(request, slug):
    group = Group.objects.get(slug=slug)
    return render(request, 'group.html', {'group': group})