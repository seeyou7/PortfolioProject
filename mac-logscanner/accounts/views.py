from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':  # Checks if the form was submitted
        form = UserRegisterForm(request.POST)
        if form.is_valid():  # validates form data
            user = form.save()  # saves the new user to the database
            login(request, user)  # logs the user in
            return redirect('dashboard')  # eedirects to the dashboard or homepage after registration
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})  # renders registration form
