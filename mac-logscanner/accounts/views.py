from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':  # Checks if the form was submitted
        form = UserRegisterForm(request.POST)
        if form.is_valid():  # Validates the form data
            user = form.save()  # Saves the new user to the database
            login(request, user)  # Logs the user in
            return redirect('dashboard')  # Redirects to the dashboard or homepage after registration
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})  # Renders the registration form
