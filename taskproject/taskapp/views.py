from django.shortcuts import render, redirect, get_object_or_404
from  .forms import *
from django.contrib.auth.hashers import make_password
from .models import *
from django.contrib.auth.hashers import check_password
from datetime import datetime, date

def index(request):
    today = date.today()
    completed_tasks_count = Task.objects.filter(Status='2', End__date=today).count()
    completed_tasks_count_2 = Task.objects.filter( End__date=today).count()
    print(completed_tasks_count)
    print(completed_tasks_count_2)
    context = {
        'completed_tasks_count': completed_tasks_count,
        'completed_tasks_count_2': completed_tasks_count_2
    }
    return render(request, 'index.html', context=context)

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
    if 'email' in request.session:
        user = get_object_or_404(User, Email=request.session['email'])
        if request.method == 'POST':
            form = AddTaskuser(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.AssignedUser = user
                task.save()
        form = AddTaskuser()
        now = datetime.now()
        tasks = MyTask.objects.filter(AssignedUser=user)

        task_1 = MyTask.objects.filter(AssignedUser=user, Status='0').count()
        task_2 = MyTask.objects.filter(AssignedUser=user, Status='1').count()
        task_3 = MyTask.objects.filter(AssignedUser=user, Status='2').count()
        user = get_object_or_404(User, Email=request.session['email'])
        return render(request, 'panel/panel.html', {'user':user, 'form': form, 'tasks': tasks, 'now': now, 'task_1': task_1, 'task_2': task_2, 'task_3': task_3})
    else:
        return redirect('/reg/')
def commandtask(request):
    user = User.objects.get(Email=request.session['email'])
    teams = Team.objects.filter(teammember__user=user, teammember__role=1)
    teams_vs = Team.objects.filter(teammember__user=user, teammember__role=2)
    teams_all = Team.objects.exclude(teammember__user=user)
    #teams_all = Team.objects.filter(teammember__isnull=False).distinct()
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
    return render(request, 'panel/commandtask.html', {'form': form, 'teams': teams, 'teams_all': teams_all, 'teams_vs': teams_vs})

def delete_team_user(request):
    if request.method == 'POST':
        id_team = request.POST['id_team']
        team = get_object_or_404(Team, id=id_team)
        user = get_object_or_404(User, Email=request.session['email'])
        team_member = get_object_or_404(TeamMember, user=user, team=team)
        team_member.delete()
    return redirect('/commandtask/')
def commandid(request, id):

    team = get_object_or_404(Team, id=id)

    team_all = TeamMember.objects.filter(team=team)

    task_list = Task.objects.filter(team=team)
    task_1 = task_list.filter(Status=0).count()
    task_2 = task_list.filter(Status=1).count()
    task_3 = task_list.filter(Status=2).count()

    teams = TeamMember.objects.filter(team=team)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.team = team
            task.save()
    form = TaskForm()
    team = Team.objects.filter(id=id).first()
    cur_user = get_object_or_404(User, Email=request.session['email'])
    tm = TeamMember.objects.filter(user=cur_user, team=team).first()



    role = tm.role.id
    users_not_in_team = User.objects.exclude(id__in=TeamMember.objects.values('user'))

    print(task_1)
    return render(request, 'panel/commandid.html', {'task_1': task_1,'task_2': task_2,'task_3': task_3, 'team': team, 'role':  role, 'form': form, 'teams': teams, 'id': id, 'users_not_in_team': users_not_in_team, 'task_list': task_list, 'team_all': team_all, 'tm': tm})

def add_team_member(request):
    if request.method == 'POST':
        t = TeamMember()
        t.team = get_object_or_404(Team, id=request.POST['id_team'])
        t.user = get_object_or_404(User, id=request.POST['id_user'])

        t.save()
        return redirect('/command/'+request.POST['id_team'])

def add_team(request):
    if request.method == 'POST':
        id_team = request.POST['id_team']
        team = get_object_or_404(Team, id=id_team)
        user =get_object_or_404(User, Email=request.session['email'])
        t = TeamMember()
        t.team = team
        t.user = user
        t.save()
    return redirect('/commandtask/')

def start_task(request):
    if request.method == 'POST':
        id_team =  request.POST['id_team']
        id_task = request.POST['id_task']
        task = get_object_or_404(Task, id=id_task)
        task.Status = '1'
        task.save()
    return redirect('/command/' + id_team)


def stop_task(request):
    if request.method == 'POST':
        id_team =  request.POST['id_team']
        id_task = request.POST['id_task']
        task = get_object_or_404(Task, id=id_task)
        task.Status = '2'
        task.save()
    return redirect('/command/' + id_team)

def deleteid(request, id):
    user = get_object_or_404(User, Email=request.session['email'])
    team_member = get_object_or_404(TeamMember, team_id=id, user=user)
    team_member.delete()
    Team.objects.get(id=id).delete()
    return redirect('/commandtask/')

def add_admin(request):
    if request.method == 'POST':
        id = request.POST['id']
        role = get_object_or_404(Role, id=1)
        task = get_object_or_404(TeamMember, id=id)
        task.role = role
        task.save()
    return redirect('/command/' + request.POST['idm'])

def mytask(request):
    user = User.objects.get(Email=request.session['email'])
    teams = Team.objects.filter(teammember__user=user, teammember__role=1)
    return render(request, 'panel/my.html',
                  {'teams': teams})

def startuser(request):
    if request.method == 'POST':
        id_task = request.POST['id_task']
        task = get_object_or_404(MyTask, id=id_task)
        task.Status = '1'
        task.save()
    return redirect('/panel/')

def stopuser(request):
    if request.method == 'POST':
        id_task = request.POST['id_task']
        task = get_object_or_404(MyTask, id=id_task)
        task.Status = '2'
        task.save()
    return redirect('/panel/')

def deleteitemid(request):
    if request.method == 'POST':
        id_task = request.POST['id_task']
        MyTask.objects.filter(id=id_task).delete()
    return redirect('/panel/')

def deleteitemidc(request):
    if request.method == 'POST':
        id_team = request.POST['id_team']
        id_task = request.POST['id_task']
        Task.objects.filter(id=id_task).delete()
    return redirect('/command/' + id_team)