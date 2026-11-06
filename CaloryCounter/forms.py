from django import forms
from django.contrib.auth.models import User
from .models import FoodLog, UserProfile


class UserRegistrationForm(forms.ModelForm):
  password = forms.CharField(
      widget=forms.PasswordInput(attrs={'class': 'form-control'})
  )
  confirm_password = forms.CharField(
      widget=forms.PasswordInput(attrs={'class': 'form-control'})
  )

  class Meta:
    model = User
    fields = ['username', 'email', 'password']
    widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.EmailInput(attrs={'class': 'form-control'}),
    }

  def clean(self):
    cleaned_data = super().clean()
    password = cleaned_data.get('password')
    confirm_password = cleaned_data.get('confirm_password')
    if password and confirm_password and password != confirm_password:
      raise forms.ValidationError('Passwords do not match!')
    return cleaned_data


class UserProfileForm(forms.ModelForm):

  class Meta:
    model = UserProfile
    fields = ['name', 'age', 'gender', 'height', 'weight']
    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'age': forms.NumberInput(attrs={'class': 'form-control'}),
        'height': forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'Height in cm'}
        ),
        'weight': forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'Weight in kg'}
        ),
        'gender': forms.Select(attrs={'class': 'form-select'}),
    }


class FoodLogForm(forms.ModelForm):

  class Meta:
    model = FoodLog
    fields = ['item_name', 'calories']
    widgets = {
        'item_name': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Chicken Biryani',
            }
        ),
        'calories': forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'e.g., 500'}
        ),
    }