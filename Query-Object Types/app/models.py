from django.db import models

# Create your models here.

class Category(models.Model):
    topic = models.CharField(max_length=250)

    def __str__(self):
        return self.topic



class Question(models.Model):
    question_text = models.TextField()
    answer_text = models.TextField(max_length=150, null=False, default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category',null=True )

    def __str__(self):
        return self.question_text