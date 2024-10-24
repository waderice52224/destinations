from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import User, Session
from .decorators import login_required_custom
import secrets
from .models import Destination


@login_required_custom
def index(request):
    destinations = Destination.objects.all()  # Get all destinations
    return render(request, 'core/places_visited.html', {'destinations': destinations})


def sign_up(req):
    if req.method == "POST":
        return redirect("/")
    else:
        return render(req, "core/sign_up.html")

def sign_in(req):
    if req.method == "POST":
        email = req.POST.get("email")
        password = req.POST.get("password")
        user = User.objects.filter(email=email).first()
        if user and user.password_hash == User.hashPassword(password):
            token = Session.objects.filter(user=user).first().token
            if token == None:
                token = secrets.token_hex(32)
                Session.objects.create(user=user, token=token)
            response = redirect('/')
            response.set_cookie("token", token)
            return response


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





@login_required_custom
def new_destination(request):
    if request.method == "POST":
        name = request.POST.get('name')
        review = request.POST.get('review')
        rating = request.POST.get('rating')
        user = request.user

        # Create a new Destination object
        Destination.objects.create(
            name=name,
            review=review,
            rating=rating,
            user=user,
            share_pub=True
        )

        return redirect('/')

    return render(request, 'core/new_destination.html')

def sign_out(request):
    token = request.COOKIES.get('token')
    if token:
        Session.objects.filter(token=token).delete()

    return redirect("/")

