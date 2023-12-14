from django.shortcuts import render, redirect, get_object_or_404
from  .forms import *
from django.contrib.auth.hashers import make_password
from .models import *
from django.contrib.auth.hashers import check_password

def index(request):
    return render(request, 'index.html')

def reg(request):
    if 'email' in request.session:
        return redirect('/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Хешируем пароль перед сохранением пользователя
            password = form.cleaned_data['password']
            hashed_password = make_password(password)

            # Создаем пользователя с хешированным паролем
            user = User(
                LastName=form.cleaned_data['LastName'],
                FirstName=form.cleaned_data['FirstName'],
                Email=form.cleaned_data['Email'],
                HashedPassword=hashed_password,
            )
            user.save()

            return redirect('/auth/')  # Перенаправление после успешной регистрации
    else:
        form = RegistrationForm()

    return render(request, 'reg.html', {'form': form})


def auth(request):
    if 'email' in request.session:
        return redirect('/')
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if User.objects.filter(Email=email).exists():
                user = User.objects.get(Email=email)
                if check_password(password, user.HashedPassword):
                    request.session['email'] = email
                    return redirect('/panel/')
            form.add_error(None, 'Неверный email или пароль.')


    else:
        form = AuthenticationForm()
    return render(request, 'auth.html', {'form': form})
def subscribers(request):
    return render(request, 'subscribers.html')
def reviews(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ReviewForm()
    reviews = Review.objects.all()
    return render(request, 'reviews.html', {'form': form, 'reviews': reviews})
def logout(request):
    if 'email' in request.session:
        del request.session['email']
    return redirect('/')
def panel(request):

    return render(request, 'panel/panel.html')

def commandtask(request):
    user = User.objects.get(Email=request.session['email'])
    teams = Team.objects.filter(teammember__user=user)
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            cur_user = get_object_or_404(User, Email=request.session['email'])
            role = get_object_or_404(Role, id=1)
            mem_team = TeamMember()
            mem_team.user = cur_user
            mem_team.role = role
            mem_team.team = team
            mem_team.save()

            #return redirect('team_list')  # Замените 'team_list' на ваш URL-маршрут для списка команд
    else:
        form = TeamForm()
    return render(request, 'panel/commandtask.html', {'form': form, 'teams': teams})

def commandid(request, id):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
    form = TaskForm()
    team = Team.objects.filter(id=id).first()
    cur_user = get_object_or_404(User, Email=request.session['email'])
    tm = TeamMember.objects.filter(user=cur_user, team=team).first()
    role = tm.role.id
    return render(request, 'panel/commandid.html', {'team': team, 'role':  role, 'form': form})