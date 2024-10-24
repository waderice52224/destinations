from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import User, Session
from .decorators import login_required_custom
import secrets
from .models import Destination


@login_required_custom
def index(req):
    return HttpResponse("<h1>Welcome to the rice fields</h1>")



def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.filter(email=email).first()

        if user and user.password_hash == user.hash_password(password):
            user.generate_token()  # Generate a new token on successful login
            request.session['user_token'] = user.token  # Store the token in the session
            return redirect('index')  # Redirect to the index page

    return render(request, "core/login.html")

def sign_up(req):
    if req.method == "POST":
        return redirect("/")
    else:
        return render(req, "core/sign_up.html")

def sign_in(req):
    # if req.method == "POST":
    #     #todo
    #     return redirect("/")
    # else:
    return render(req, "core/sign_in.html")

def new_user(req):
    if req.method == 'POST':
        name = req.POST.get('name')
        email = req.POST.get('email')
        password = req.POST.get('password')
        password_hash = User.hashPassword(password)


        user = User.objects.create(name=name, email=email, password_hash=password_hash)
        token = secrets.token_hex(32)
        Session.objects.create(user=user, token=token)

        response = redirect('/')
        response.set_cookie("token", token)
        return response

    return render(req, '/', {'error_message': '400 Error: Message was not a POST'})


def places_visited(request):
    destinations = Destination.objects.all()  # Get all destinations
    return render(request, 'core/places_visited.html', {'destinations': destinations})


@login_required_custom
def new_destination(request):
    if request.method == "POST":
        name = request.POST.get('name')
        review = request.POST.get('review')
        rating = request.POST.get('rating')
        user = request.user  # Assuming you have user authentication set up

        # Create a new Destination object
        Destination.objects.create(
            name=name,
            review=review,
            rating=rating,
            user=user,
            share_publicly=True  # Assuming you want to share by default
        )

        return redirect('places_visited')  # Redirect to the places visited page

    return render(request, 'core/new_destination.html')