from django.contrib import admin
from .models import User, Workshop, TeamMember, Events 

# Register your models here.
admin.site.register(User)
admin.site.register(Workshop)
admin.site.register(TeamMember)
admin.site.register(Events)
