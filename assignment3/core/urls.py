
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('new_destination/', views.new_destination, name='new_destination'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('new_user/', views.new_user, name='new_user')
]


