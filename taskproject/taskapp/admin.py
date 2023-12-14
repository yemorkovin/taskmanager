from django.contrib import admin
from .models import *

admin.site.register(RoleUser)
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(Task)