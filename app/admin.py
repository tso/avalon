from app.models import Game, Player, User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(Game)
admin.site.register(Player)
admin.site.register(User, UserAdmin)
