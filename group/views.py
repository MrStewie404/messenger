from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from .models import Group, Message
from main.models import Avatars
from .forms import GroupForm

@login_required
def groups(request):
    groups = Group.objects.all()
    return render(request, 'groups.html', {'groups': groups})

@login_required
def group(request, slug):
    group = Group.objects.get(slug=slug)
    messages = Message.objects.filter(group=group)
    if messages:
        user = messages.first().user
        avatars = user.avatars.first()
    else:
        user = avatars =  None

    return render(request, 'group.html', {'group': group, 'messages': messages, 'avatars': avatars})

@login_required
def group_add(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        form.instance.creator = request.user
        if form.is_valid():
            form.save()
            return redirect('groups')
    else:
        form = GroupForm()
    return render(request, 'group_add.html', {'form': form})

def group_edit(request, slug):
    if request.method == 'POST':
        group = get_object_or_404(Group, slug=slug)
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('groups')
    elif request.method == 'GET':
        group = get_object_or_404(Group, slug=slug)
        form = GroupForm(instance=group)
    else:
        form = GroupForm()
    return render(request, 'group_edit.html', {'form': form, 'slug': slug})

def group_delete(request, slug):
    if request.method == 'GET':
        group = Group.objects.get(slug=slug)
        group.delete()
    return HttpResponseRedirect('/groups/')