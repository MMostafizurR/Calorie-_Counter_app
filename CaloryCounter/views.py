from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from .forms import FoodLogForm, UserProfileForm, UserRegistrationForm
from .models import FoodLog, UserProfile

# Create your views here.
def register_view(request):
  if request.method == 'POST':
    user_form = UserRegistrationForm(request.POST)
    profile_form = UserProfileForm(request.POST)
    if user_form.is_valid() and profile_form.is_valid():
      user = user_form.save(commit=False)
      user.set_password(user_form.cleaned_data['password'])
      user.save()

      profile = profile_form.save(commit=False)
      profile.user = user
      profile.save()

      login(request, user)
      return redirect('dashboard')
  else:
    user_form = UserRegistrationForm()
    profile_form = UserProfileForm()

  return render(
      request,
      'register.html',
      {'user_form': user_form, 'profile_form': profile_form},
  )


def login_view(request):
  if request.method == 'POST':
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      return redirect('dashboard')
  else:
    form = AuthenticationForm()
  return render(request, 'login.html', {'form': form})


def logout_view(request):
  logout(request)
  return redirect('login')


@login_required
def dashboard_view(request):
  profile = get_object_or_404(UserProfile, user=request.user)

  # Calculate BMR using Harris-Benedict formulas from specs
  if profile.gender == 'Male':
    bmr = (
        66.47
        + (13.75 * profile.weight)
        + (5.003 * profile.height)
        - (6.755 * profile.age)
    )
  else:
    bmr = (
        655.1
        + (9.563 * profile.weight)
        + (1.850 * profile.height)
        - (4.676 * profile.age)
    )

  # Simple guidelines for weight adjustment
  weight_loss_target = bmr - 500
  weight_gain_target = bmr + 500

  # Fetch daily consumed food logs & total calories
  food_logs = FoodLog.objects.filter(user=request.user).order_by('-id')
  total_consumed = sum(log.calories for log in food_logs)

  context = {
      'profile': profile,
      'bmr': round(bmr, 2),
      'weight_loss_target': round(weight_loss_target, 2),
      'weight_gain_target': round(weight_gain_target, 2),
      'food_logs': food_logs,
      'total_consumed': total_consumed,
  }
  return render(request, 'dashboard.html', context)


@login_required
def add_food_view(request):
  if request.method == 'POST':
    form = FoodLogForm(request.POST)
    if form.is_valid():
      food_log = form.save(commit=False)
      food_log.user = request.user
      food_log.save()
      return redirect('dashboard')
  else:
    form = FoodLogForm()
  return render(request, 'add_food.html', {'form': form})