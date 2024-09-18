from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.conf import settings
from .models import Avatars, Updates
from .forms import SignUpForm, LoginForm, UserForm, AvatarForm, UpdateForm
import os

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_detail(request, pk):
    user = User.objects.get(pk=pk)
    try:
        avatar = Avatars.objects.get(user=user)
    except:
        Avatars.objects.create(user=user)
        avatar = Avatars.objects.get(user=user)
    return render(request, 'profile.html', {'user': user, 'avatar': avatar})

def avatar_view(filename):
    image_path = os.path.join(settings.STATIC_URL, 'avatars', filename)
    with open(image_path, 'rb') as f:
        image_data = f.read()
    return HttpResponse(image_data, content_type='image')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def update_profile(request, pk):
    user = request.user
    avatar = Avatars.objects.get(user=user)
    avatar_last_path = avatar.path
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        avatar_form = AvatarForm(request.POST, request.FILES, instance=avatar)

        
        if user_form.is_valid() and avatar_form.is_valid():
            try:
                os.remove(str(settings.BASE_DIR) + '/static/media/avatars/' + str(avatar_last_path))
            except:
                ...
            user_form.save()
            avatar_form.save()
            return redirect(f'/profile/{user.pk}')
    else:
        user_form = UserForm(instance=user)
        avatar_form = AvatarForm(instance=avatar)

    context = {
        'user_form': user_form,
        'avatar_form': avatar_form,
    }
    
    return render(request, 'update_profile.html', context)

# class UpdatesListView(ListView):
#     model = Updates
#     template_name = 'updates.html'
#     context_object_name = 'updates'

#     def get_queryset(self):
#         return super().get_queryset().order_by('-date')

def base(request):
    updates = Updates.objects.all().order_by('-date')
    users = User.objects.all()

    return render(request, 'updates.html', {'updates': updates, 'users': users})

class UpdatesDetailView(DetailView):
    model = Updates
    template_name = 'update.html'
    context_object_name = 'update'

def update_create(request):
    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('updates')
    else:
        form = UpdateForm()
    return render(request, 'create_update.html', {'form': form})

def login_redirect(request):
    return redirect('/')