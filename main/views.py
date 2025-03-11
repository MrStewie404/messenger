from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.conf import settings
from .models import *
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from .forms import *
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
        description = UserSupplement.objects.get(user=user)
    except:

        # TODO УДАЛИТЬ ПЕРЕД РЕЛИЗОМ
        avatars = Avatars.objects.filter(user=user)
        for avatar in avatars:
            avatar.delete()
        
        descriptions = UserSupplement.objects.filter(user=user)
        for description in descriptions:
            description.delete()

        Avatars.objects.create(user=user)
        UserSupplement.objects.create(user=user)
        avatar = Avatars.objects.get(user=user)
        description = UserSupplement.objects.get(user=user)

    modules = AddedModules.objects.filter(user=user, visible=True)
    added_modules = list(AddedModules.objects.filter(user=user, visible=True))

    # Получаем или создаем последовательность модулей
    sequence_obj, created = ModuleSequence.objects.get_or_create(user=user, defaults={'modules_id': []})

    # Если список пуст, создаем последовательность в виде [[id1], [id2], [id3]]
    if not sequence_obj.modules_id:
        sequence_obj.modules_id = [[mod.id] for mod in added_modules]
        sequence_obj.save()

    # Создаем отображение id -> объект
    module_dict = {mod.id: mod for mod in added_modules}

    # Формируем двумерный массив, заменяя id на реальные объекты
    modules = [[module_dict[obj] for obj in row['modules'] if obj in module_dict.keys()] for row in sequence_obj.modules_id]

    return render(request, 'profile.html', {
        'user': user, 
        'avatar': avatar, 
        'modules': modules,
        'description': description
    })

def favicon(filename):
    image_path = os.path.join(settings.STATIC_URL, 'default/favicon_io', filename)
    with open(image_path, 'rb') as f:
        image_data = f.read()
    return HttpResponse(image_data, content_type='image')

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
@xframe_options_exempt
# def update_profile(request, pk):
#     user = request.user
#     avatar = Avatars.objects.get(user=user)
#     all_modules = Modules.objects.filter(user=request.user)
#     user_modules = AddedModules.objects.filter(user=request.user)
#     avatar_last_path = avatar.path

#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=user)
#         avatar_form = AvatarForm(request.POST, request.FILES, instance=avatar)
#         # Изменяем формирование формы, чтобы использовать отфильтрованный Queryset
#         modules_form = ModulesChoiceForm(request.POST, queryset=all_modules)

#         if user_form.is_valid() and avatar_form.is_valid() and modules_form.is_valid():
#             try:
#                 os.remove(str(settings.BASE_DIR) + '/static/media/avatars/' + str(avatar_last_path))
#             except:
#                 ...
#             user_form.save()
#             avatar_form.save()
#             selected_modules = modules_form.cleaned_data['modules']

#             # Обновляем поле visible в модели
#             for module in all_modules:
#                 module.visible = module in selected_modules # если модуль выбран - True, иначе - False
#                 module.save()

#             return redirect(f'/profile/{user.pk}/edit/')
#     else:
#         user_form = UserForm(instance=user)
#         avatar_form = AvatarForm(instance=avatar)
#         # Изменяем формирование формы, чтобы использовать отфильтрованный Queryset и инициализацию
#         modules_form = ModulesChoiceForm(queryset=all_modules, initial={'modules': user_modules.filter(visible=True)})

#     context = {
#         'user_form': user_form,
#         'avatar_form': avatar_form,
#         'modules': all_modules,
#         'modules_form': modules_form,
#     }

#     return render(request, 'update_profile.html', context)

# views.py
def your_view(request):
    queryset = AddedModules.objects.all()  # Или ваш кастомный queryset
    form = ModulesChoiceForm(queryset=queryset)
    
    # Связываем элементы формы и queryset
    zipped_data = zip(form["modules"], queryset)
    
    return render(request, "your_template.html", {
        "form": form,
        "zipped_data": zipped_data,
    })

def update_profile(request, pk):
    avatar = Avatars.objects.get(user=request.user)
    user_modules = AddedModules.objects.filter(user=request.user)
    user_description = UserSupplement.objects.get(user=request.user)
    avatar_last_path = avatar.path

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        avatar_form = AvatarForm(request.POST, request.FILES, instance=avatar)
        description_form = DescriptionForm(request.POST, instance=user_description)
        # Изменяем формирование формы, чтобы использовать отфильтрованный Queryset
        if user_form.is_valid() and avatar_form.is_valid() and description_form.is_valid():
            try:
                os.remove(str(settings.BASE_DIR) + '/static/media/avatars/' + str(avatar_last_path))
            except:
                ...
            user_form.save()
            avatar_form.save()
            description_form.save()
            # selected_modules = modules_form.cleaned_data['modules']

            # Обновляем поле visible в модели
            # for module in user_modules:
            #     module.visible = module in selected_modules # если модуль выбран - True, иначе - False
            #     module.save()

            return redirect(f'/profile/{request.user.pk}/edit/')
        print(description_form.errors)
    else:
        user_form = UserForm(instance=request.user)
        avatar_form = AvatarForm(instance=avatar)
        description_form = DescriptionForm(instance=user_description)
        # Изменяем формирование формы, чтобы использовать отфильтрованный Queryset и инициализацию
    
    for i in range(len(user_modules)):
        user_modules[i].visible = json.dumps(user_modules[i].visible)
        user_modules[i].visibility_for_others = json.dumps(user_modules[i].visibility_for_others)
    

    context = {
        'user_form': user_form,
        'avatar_form': avatar_form,
        'modules': user_modules,
        'description_form': description_form,
    }

    return render(request, 'update_profile.html', context)

class UpdatesListView(ListView):
    model = Updates
    template_name = 'updates.html'
    context_object_name = 'updates'

    def get_queryset(self):
        return super().get_queryset().order_by('-date')

def base(request):
    updates = Updates.objects.all().order_by('-date')
    users = User.objects.all()

    if not request.user.id:
        return render(request, 'base.html', {'updates': updates, 'user_count': len(users)-1})
    else:
        return redirect(f'/profile/{request.user.id}')

# def module_search(request):
#     modules = Modules.objects.filter(visible_in_public=True)
#     return render(request, 'modules.html', {'modules': modules})

def module_search(request):
    form = ModulesFormSearch()
    query_results = []

    # Если пользователь отправил форму (POST-запрос)
    if request.method == 'POST':
        form = ModulesFormCreate(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем новый модуль
            form = ModulesFormSearch()  # Сбрасываем форму после сохранения

    # Если пользователь подал запрос с фильтрацией (GET-запрос)
    elif request.method == 'GET':
        search_query = request.GET.get('search', '')  # Получаем поисковый запрос из строки запроса
        if search_query:
            # Поиск производится по полям name или description
            query_results = Modules.objects.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        else:
            query_results = Modules.objects.all()

    context = {
        'form': form,
        'query_results': query_results
    }
    return render(request, 'modules.html', context)

@login_required
def modules_create(request):
    if request.method == 'POST':
        form = ModulesFormCreate(request.POST, request.FILES)
        if form.is_valid():
            module = form.save(commit=False)
            module.user = request.user
            module.save()
            AddedModules.objects.create(module=module, user=request.user)

            # Сохранить переданный файл, если нужно
            uploaded_file = request.FILES.get('path')
            if uploaded_file:
                target_dir = os.path.join(
                    settings.BASE_DIR,
                    'static',
                    'modules',
                    str(request.user.id)
                )
                os.makedirs(target_dir, exist_ok=True)
                file_path = os.path.join(target_dir, uploaded_file.name)
                with open(file_path, 'wb') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
                module.path = os.path.join('modules', str(request.user.id), uploaded_file.name)

            module.save()
            return redirect(f'/profile/{request.user.id}')
        else:
            print(form.errors)
            print(form.module_details_formset.errors)
    else:
        form = ModulesFormCreate()
    return render(request, 'modules_create.html', {'form': form})


def modules_add(request, pk):
    module = Modules.objects.get(id=pk)
    try:
        visibility_for_others = True if len(request.GET.get('visible-for-other')) == 4 else False
        visible = True if len(request.GET.get('visible')) == 4 else False
        height = int(request.GET.get('height'))
        width = int(request.GET.get('width'))
    except:
        visibility_for_others = False
        visible = True
        height = width = 0

    AddedModules.objects.create(user=request.user, 
                                module=module, 
                                visibility_for_others=visibility_for_others, 
                                visible=visible,
                                height=height,
                                width=width
    )
    return render(request, 'close.html')

def modules_del(request, pk):
    try:
        module = AddedModules.objects.get(id=pk)

        created_module = Modules.objects.get(id = module.module.id)
        print(request.user, created_module.user)
        if request.user == created_module.user:
            Modules.objects.get(id = module.module.id).delete()
        else:
            module.delete()

        return redirect(f'/profile/{request.user.id}/edit')
    except Exception as e:
        print(e)
        return redirect(f'/profile/{request.user.id}/edit')

def modules_upd(request, pk):
    module = get_object_or_404(AddedModules, id=pk, user=request.user)
    
    if request.method == "POST":
        form = ModuleDetailsForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Модуль успешно обновлён'
            })
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    return JsonResponse({'status': 'invalid_request'}, status=400)

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

def update_update(request, pk):
    update = Updates.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=update)
        if form.is_valid():
            form.save()
            return redirect(f'/update/{update.id}')
    else:
        form = UpdateForm(instance=update)
    return render(request, 'update_update.html', {'form': form})

def update_delete(request, pk):
    update = Updates.objects.get(id=pk)
    update.delete()
    return redirect('updates')
    

def login_redirect(request):
    return redirect('/')

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def module_update_sequence(request):
    if request.method == 'POST':
        try:
            # Парсим данные из тела запроса (ожидается JSON)
            data = json.loads(request.body)

            try:
                do = data.get('do')
            except:
                do = "nothing"
            user_id = data.get('user_id')
            sequence = data.get('sequence')

            if "update" == do:
                # Проверяем, существует ли сущность с таким user_id
                if ModuleSequence.objects.filter(user_id=user_id).exists():
                    # Если существует, обновляем записи
                    ModuleSequence.objects.filter(user_id=user_id).update(modules_id=sequence)
                    return JsonResponse({'message': 'has been updated'}, status=200)  # Ответ с кодом 200 - успешно
                else:
                    # Если сущности нет, создаём новую
                    ModuleSequence.objects.create(user_id=user_id, modules_id=sequence)
                    return JsonResponse({'message': 'has been created'}, status=200)  # Ответ с кодом 200 - успешно
            elif "get" == do:
                # Проверяем, существует ли сущность с таким user_id
                if ModuleSequence.objects.filter(user_id=user_id).exists():
                    sequence = ModuleSequence.objects.get(user_id=user_id)
                    return JsonResponse({'message': 'your welcome', 'user_id': sequence.user.id, 'modules': sequence.modules_id}, status=200)  # Ответ с кодом 200 - успешно
                else:
                    return JsonResponse({'error': 'check user_id'}, status=400)  # Ответ с кодом 200 - успешно
            else:
                return JsonResponse({'error': 'i dont know what u want. update or get? please, tald me that in "do"'}, status=400)  # Ответ с кодом 200 - успешно

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
