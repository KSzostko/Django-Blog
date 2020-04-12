from django.db import models
from django.contrib import auth


class User(auth.models.User):

    def __str__(self):
        return f'{self.username}'
