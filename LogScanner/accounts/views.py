from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm # to imple later

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
       
        if form.is_valid():
            user = form.save()
            login(request, user)
            #log user in afte registering
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
         #messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/register.html', {'form': form})