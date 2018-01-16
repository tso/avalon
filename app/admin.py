from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app.models import Game, Player, User

# Register your models here.
admin.site.register(Game)
admin.site.register(Player)
admin.site.register(User, UserAdmin)
