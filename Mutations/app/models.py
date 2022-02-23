from django.db import models

# Create your models here.
class Category(models.Model):
    topic = models.CharField(max_length=250)

    def __str__(self):
        return self.topic

class Pet(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name