from django.shortcuts import render, redirect
from .models import Restaurant
from .forms import RestaurantForm
from .forms import SignupForm
from .forms import SigninForm
from django.contrib.auth import login,logout,authenticate

# Create two forms, one for signing up and one for signing in.
# Form for signing up should be called SignupForm.
# Form for signing in should be called SigninForm.
# Create a Sign-up view. It has been partially written for you, complete it.
# Create a Sign-in view. It has been partially written for you, complete it.
# Create a Sign-out view.
# The URLs have already been written for you.
# Create a link for the authentication views in the nav-bar.
# Pass the tests.
# Push your code.

def signup(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.set_password(obj.password)
            obj.save()
            login(request,obj)
            return redirect('restaurant-list')
    context = {
        "form":form,
    }
    return render(request, 'signup.html', context)



def signin(request):
    form = SigninForm()
    if request.method == "POST":
        form = SigninForm(request.POST, request.FILES)
        if form.is_valid():
            my_user=form.cleaned_data['username']
            my_pass=form.cleaned_data['password']
            ob=authenticate(username=my_user,password=my_pass)
            if ob is not None:
                login(request,ob)
                return redirect('restaurant-list')
    context = {
        "form":form,
    }
    return render(request, 'signin.html', context)



def signout(request):
    logout(request)
    return redirect('signin')

def restaurant_list(request):
    context = {
        "restaurants":Restaurant.objects.all()
    }
    return render(request, 'list.html', context)


def restaurant_detail(request, restaurant_id):
    context = {
        "restaurant": Restaurant.objects.get(id=restaurant_id)
    }
    return render(request, 'detail.html', context)

def restaurant_create(request):
    form = RestaurantForm()
    if request.method == "POST":
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('restaurant-list')
    context = {
        "form":form,
    }
    return render(request, 'create.html', context)

def restaurant_update(request, restaurant_id):
    restaurant_obj = Restaurant.objects.get(id=restaurant_id)
    form = RestaurantForm(instance=restaurant_obj)
    if request.method == "POST":
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant_obj)
        if form.is_valid():
            form.save()
            return redirect('restaurant-list')
    context = {
        "restaurant_obj": restaurant_obj,
        "form":form,
    }
    return render(request, 'update.html', context)

def restaurant_delete(request, restaurant_id):
    restaurant_obj = Restaurant.objects.get(id=restaurant_id)
    restaurant_obj.delete()
    return redirect('restaurant-list')
