from django.urls import path
from . import views
from .views import liste_smartphones
from django.contrib import admin


import requests
urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('/admin', admin.site.urls, name='admin'),
    path('smartphones/', liste_smartphones , name='liste_smartphones'),
    path('skander', views.rechercher_smartphones, name='rechercher_smartphones'),
    path('create-account/', views.create_account, name='create_account'),  # Nouvelle URL pour la création de compte
    path('create_user/', views.create_user, name='create_user'),
    path('stat/', views.smartphone_price_chart , name='smartphone_price_chart'),
    path('login/',views.login_view,name='login')




]