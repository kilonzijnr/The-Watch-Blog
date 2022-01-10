from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from .models import Hood, Location, Post, User,NeighbourHood
from .forms import  NeighbourHoodForm,PostForm,UpdateProfileForm

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

def create_hood(request):
    """View functionality for creating a new neighbourhood"""
    if request.method == 'POST':
        form = NeighbourHoodForm(request.POST, request.FILES)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.admin = request.user.profile
            hood.save()
            return redirect('hood')   

    else:
        form = NeighbourHoodForm()
    return render(request, 'newhood.html', {'form': form})

def create_post(request, hood_id):
    """View functionality for creating a news post"""
    hood = NeighbourHood.objects.get(id=hood_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.hood = hood
            post.user = request.user.profile
            post.save()
            return redirect('single-hood', hood.id)
    else:
        form = PostForm()
    return render(request, 'post.html', {'form': form})

def profile(request, username):
    """View functionality for user profile"""
    return render(request, 'profile.html')   

def edit_profile(request, username):
    """View functionality for editing user profile"""
    user = User.objects.get(username=username)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile', user.username)
    else:
        form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'profile_update.html', {'form': form})

def join_hood(request, id):
    """View functionality for joining a new hood"""
    neighbourhood = get_object_or_404(NeighbourHood, id=id)
    request.user.profile.neighbourhood = neighbourhood
    request.user.profile.save()
    return redirect('hood')

def leave_hood(request, id):
    """Functionality for exiting a hood you had joined"""
    hood = get_object_or_404(NeighbourHood, id=id)
    request.user.profile.neighbourhood = None
    request.user.profile.save()
    return redirect('hood')   
