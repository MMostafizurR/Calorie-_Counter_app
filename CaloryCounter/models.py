from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserProfile(models.Model):
  GENDER_CHOICES = [
      ('Male', 'Male'),
      ('Female', 'Female'),
  ]

  user = models.OneToOneField(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  age = models.IntegerField()
  gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
  height = models.FloatField(help_text='Height in cm')
  weight = models.FloatField(help_text='Weight in kg')

  def __str__(self):
    return self.name


class FoodLog(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  item_name = models.CharField(max_length=150)
  calories = models.IntegerField()
  date_logged = models.DateField(auto_now_add=True)

  def __str__(self):
    return f'{self.item_name} ({self.calories} kcal)'