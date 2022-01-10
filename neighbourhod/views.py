from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from .models import Hood, Location, Post, User

# Create your views here.
def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('homepage')


    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try: 
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user doesnt exist')

        user = authenticate(request, username= username, password=password)

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'username or password does not exist')

    context = {
        'page':page
    }
    return render(request, 'registration/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('homepage')

def registerUser(request):
    page = 'register'
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'An error occured during registration')
    context = {
        'form':form,
        'page':page
    }

    return render(request, 'registration/login.html', context)

def homepage(request):
    pst = request.GET.get('pst') if request.GET.get('pst') != None else ''

    hoods = Hood.objects.filter(pst(location__name__icontains=pst) | pst(name__icontains=pst))
    locations = Location.objects.all()
    hood_count = hoods.count()
    posts = Post.objects.filter(pst(hood__location__name__icontains=pst))

    context = {
        'hoods':hoods,
        'locations':locations,
        'hood_count':hood_count, 
        'posts':posts
    }
    return render(request, 'home.html', context)