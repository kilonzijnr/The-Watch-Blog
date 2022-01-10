from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from .models import   Post, User,NeighbourHood,Business,Profile
from .forms import  NeighbourHoodForm,PostForm,UpdateProfileForm,BusinessForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('hoods')


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
            return redirect('hoods')
        else:
            messages.error(request, 'username or password does not exist')

    context = {
        'page':page
    }
    return render(request, 'registration/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('hoods')

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
            return redirect('hoods')
        else:
            messages.error(request, 'An error occured during registration')
    context = {
        'form':form,
        'page':page
    }

    return render(request, 'registration/login.html', context)


@login_required(login_url='login')
def create_hood(request):
    """View functionality for creating a new neighbourhood"""
    if request.method == 'POST':
        form = NeighbourHoodForm(request.POST, request.FILES)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.admin = request.user.profile
            hood.save()
            return redirect('hoods')   

    else:
        form = NeighbourHoodForm()
    return render(request, 'newhood.html', {'form': form})

@login_required(login_url='login')
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

@login_required(login_url='login')
def profile(request, username):
    """View functionality for user profile"""
    return render(request, 'profile.html')   

@login_required(login_url='login')
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

def hoods(request):
    """View Functionality for getting all hoods"""
    all_hoods = NeighbourHood.objects.all()
    all_hoods = all_hoods[::-1]
    params = {
        'all_hoods': all_hoods,
    }
    return render(request, 'home.html', params)

@login_required(login_url='login')
def join_hood(request, id):
    """View functionality for joining a new hood"""
    neighbourhood = get_object_or_404(NeighbourHood, id=id)
    request.user.profile.neighbourhood = neighbourhood
    request.user.profile.save()
    return redirect('hoods')

@login_required(login_url='login')
def leave_hood(request, id):
    """Functionality for exiting a hood you had joined"""
    hood = get_object_or_404(NeighbourHood, id=id)
    request.user.profile.neighbourhood = None
    request.user.profile.save()
    return redirect('hoods')   

@login_required(login_url='login')
def search_business(request):
    """Functionality for searching for a bussiness by a specific name"""
    if request.method == 'GET':
        name = request.GET.get("title")
        results = Business.objects.filter(name__icontains=name).all()
        print(results)
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'results.html', params)
    else:
        message = "You haven't searched for any image category"
    return render(request, "search.html")         

@login_required(login_url='login')
def single_hood(request, hood_id):
    """Functionality for getting a single hood"""
    hood = NeighbourHood.objects.get(id=hood_id)
    business = Business.objects.filter(neighbourhood=hood)
    posts = Post.objects.filter(hood=hood)
    posts = posts[::-1]
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            b_form = form.save(commit=False)
            b_form.neighbourhood = hood
            b_form.user = request.user.profile
            b_form.save()
            return redirect('single-hood', hood.id)
    else:
        form = BusinessForm()
    params = {
        'hood': hood,
        'business': business,
        'form': form,
        'posts': posts
    }
    return render(request, 'hood.html', params)     

@login_required(login_url='login')
def hood_members(request, hood_id):
    """Function for getting all hood members"""
    hood = NeighbourHood.objects.get(id=hood_id)
    members = Profile.objects.filter(neighbourhood=hood)
    return render(request, 'members.html', {'members': members}) 

@login_required(login_url='login')
def createBusiness(request):
    """View functionality for creating a new neighbourhood"""
    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.admin = request.user.profile
            business.save()
            return redirect('hoods')   

    else:
        form = BusinessForm()
    return render(request, 'new_business.html', {'form': form})