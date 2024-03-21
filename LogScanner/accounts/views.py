#r html temp et passer contexte to it
from django.shortcuts import render, redirect
from django.contrib.auth import login #(auth sys)
from .forms import UserRegisterForm 


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)# instantiate urf withdata form requ.post
       #ok submitted data sent to serv trought meth POST en for dic
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













# A POST request typically indicates a user's intent to submit data they've entered into a form. Checking for a POST request allows the server to distinguish between a user simply requesting the form (via a GET request) and a user intending to submit the form (via a POST request).
#Django's Cross Site Request Forgery (CSRF) protection mechanism works by checking for a CSRF token in POST requests. 
#By handling form submissions with POST requests, you ensure that CSRF protection is applied.