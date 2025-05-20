from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    telefone = models.CharField(max_length=20, blank=True)
    endereco = models.TextField(blank=True)

    def __str__(self):
        return self.username