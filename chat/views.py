from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.contrib.auth.models import User
from .models import Chat, Message
from django.db.models import Q

@login_required
def chats(request):
    user = request.user
    chats = Chat.objects.filter(Q(user1=user) | Q(user2=user)).distinct()

    cleared_chats = []
    for chat in chats:
        if chat.user1 != user:
            chat.user = chat.user1
            cleared_chats.append(chat)
        elif chat.user2 != user:
            chat.user = chat.user2
            cleared_chats.append(chat)
    
    # users_id = chats.user
    # users = User.objects.filter(id__in=users_id)

    # user_avatars = {}
    # for user in users:
    #     avatar = user.avatars.first()
    #     user_avatars[user.id] = avatar.path.url


    return render(request, 'chats.html', {'chats': cleared_chats}) 

@login_required
def chat(request, id):
    messages = Message.objects.filter(chat_id=id)
    return render(request, 'chat.html', {'messages': messages, 'chat_id': id})

@login_required
def chat_search(request):
    query = request.GET.get('q', '')
    query = request.GET.get('q', '')
    chats = user = []
    if query:
        if '@' in query:
            user = User.objects.filter(username__icontains=query.replace('@', ''))

            for u in user:
                chats.extend(Chat.objects.filter(Q(user1=u) & Q(user2=request.user) | 
                                                Q(user2=u) & Q(user1=request.user)).distinct())

    print(chats)
    cleared_chats = []
    for chat in chats:
        if chat.user1 != request.user:
            chat.user = chat.user1
            cleared_chats.append(chat)
        elif chat.user2 != request.user:
            chat.user = chat.user2
            cleared_chats.append(chat)

    
    context = {'chats': cleared_chats, 'user_searched': user, 'query': query}
    return render(request, 'chat_search.html', context)

# @login_required
# def chat_search(request):
#     query = request.GET.get('q', '')
#     users = chats = []
#     if query:
#         print(query)
#         if '@' in query:
#             users = User.objects.get(username__icontains=query.replace('@', ''))
#             chats = Chat.objects.filter(Q(user1=users) | Q(user2=users)).distinct()
#         else:
#             users = User.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
#             # chats = Chat.objects.filter(Q(user1=users) | Q(user2=users)).distinct()
    
#     print(users)

#     context = {'users': users, 'chats': chats, 'query': query}
#     return render(request, 'chat_search.html', context)

@login_required
def create_chat(request, id):
    user = User.objects.get(id=id)
    chat = Chat.objects.create(user1=request.user, user2=user)
    return HttpResponseRedirect(f'/chats/{chat.id}')