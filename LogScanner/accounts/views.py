#r html temp et passer contexte to it
from django.shortcuts import render, redirect
from django.contrib.auth import login #(auth sys)
from .forms import UserRegisterForm 


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)# pople le dict with all info 
       #ok submitted data sent to serv trought meth POST en for dic'champ:younes'
        if form.is_valid():
            user = form.save()
            login(request, user)#connection
            #log user in afte registering
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
         #messages.error(request, 'Invalid username or password') to check later when dashbork isOK
    return render(request, 'accounts/register.html', {'form': form})
    # un trasmitteur de inst de v htmltemp fonctionne bien prob regler

