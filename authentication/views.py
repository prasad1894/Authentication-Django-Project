from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    
    if request.method == "POST":
        #username = request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if User.objects.filter(username=username):
            messages.error(request, "username already exists try another username")
            return redirect('home')
            
        #if User.objects.filter(email=email):
            #messages.error(request, "email already registered")
            #return redirect('home')
        
        if len(username)>10:
            messages.error(request, "username must be under 10 characters")
            
        if password != password2:
            messages.error(request, "passwords does not match")
            
        if not username.isalnum():
            messages.error(request, "username must be alpha-numeric")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        
        myuser.save()
        
        messages.success(request, "Account has been Successfully Created")
        
        return redirect('signin')
    
    
    
    return render(request, "authentication/signup.html")

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            lname = user.last_name
            return render(request, "authentication/index.html", {'lname': lname})
        
        else:
            messages.error(request, "Incorrect Details")
            return redirect('home')
        
    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged  Out Successfully")
    return redirect('home')