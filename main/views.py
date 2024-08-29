from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .forms import SignUpForm, LoginForm
# from .models import User, Chat

def base(request):
    return render(request, 'base.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('base')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

class UserDetail(DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user'

# class ChatView(ListView):
#     model = Chat
#     template_name = 'chats.html'
#     context_object_name = 'chats'


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('base')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('base')

# def register_view(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')  # Перенаправление на страницу входа
#     else:
#         form = UserForm()
#     return render(request, 'register.html', {'form': form})

# def logout_view(request):
#     logout(request)
#     return redirect('login')  # Перенаправляем на страницу входа