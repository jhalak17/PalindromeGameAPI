from django.db import models

# Create your models here.
class UserModel(models.Model):
    email = models.EmailField(unique = True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=15)
    password2 = models.CharField(max_length=15)

class GameModel(models.Model):
    game_id = models.IntegerField(unique=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    game_string = models.CharField(max_length=6, default = 0)
    is_palindrome = models.BooleanField(default = False)