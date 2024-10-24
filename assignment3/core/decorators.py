from django.shortcuts import render, redirect
from .models import Session


def login_required_custom(view_func):
    def wrapped_func(req):
        token = req.COOKIES.get('token')

        session = Session.objects.filter(token=token).first()
        if session is not None:
            req.user = session.user
            return view_func(req)
        else:
            return redirect("sign_in")
    return wrapped_func