from django.db import models

# Create your models here.
class Subscribes(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=120)
    tel = models.CharField(max_length=20)

    # вывод одного поля
    # def __str__(self):
    #     return self.name