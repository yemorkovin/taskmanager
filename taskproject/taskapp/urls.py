"""
URL configuration for taskproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from .views import *
urlpatterns = [
    path('', index),
    path('reg/', reg, name='registration_view'),
    path('auth/', auth, name='auth_view'),
    path('reviews/', reviews, name='reviews'),
    path('panel/', panel, name='panel'),
    path('logout/', logout, name='logout'),
    path('subscribers/', subscribers, name='subscribers'),
    path('commandtask/', commandtask, name='commandtask'),
    path('command/<int:id>', commandid),
    path('add_team_member/', add_team_member, name='add_team_member'),
    path('add_team/', add_team, name='add_team_user'),
    path('delete_team_user/', delete_team_user, name='delete_team_user'),
    path('start_task/', start_task, name='start_task'),
    path('stop_task/', stop_task, name='stop_task'),
    path('delete/<int:id>', deleteid, name='deleteid'),
    path('add_admin/', add_admin, name='add_admin'),
    path('mytask/', mytask, name='mytask')
]
