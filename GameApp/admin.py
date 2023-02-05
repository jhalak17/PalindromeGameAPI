from django.contrib import admin

# Register your models here.
from .models import UserModel, GameModel

@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email"]

@admin.register(GameModel)
class GameAdmin(admin.ModelAdmin):
    list_display = ["id", "game_id", "user", "game_string", "is_palindrome"]

