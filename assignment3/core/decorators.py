from django.shortcuts import render


def login_required_custom(view_func):
    def wrapped_func(req):
        token = req.session.get('user_token')
        print(token)
        if req.user.is_authenticated:
            return view_func(req)
        else:
            # Redirect to login page
            return render(req, "core/sign_in.html")
    return wrapped_func