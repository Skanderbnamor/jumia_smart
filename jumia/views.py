from io import BytesIO
import json
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from .models import Smartphone  # Importez votre modèle Smartphone
from django.contrib.auth.models import User
from django.contrib import messages
import sqlite3
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render
import matplotlib.pyplot as plt


def hello_world(request):
    return render(request, 'hello.html')


def create_account(request):
    return render(request, 'create_account.html')


def liste_smartphones(request):
    smartphones = Smartphone.objects.all()  # Récupérez tous les smartphones de la base de données
    return render(request, 'liste_smartphones.html', {'smartphones': smartphones})


def rechercher_smartphones(request):
    # Charger les données JSON
    with open(r'C:\Users\skand\PycharmProjects\jumia_smart\smartphones.json', 'r', encoding='utf8') as f:
        smartphones = json.load(f)

    # Récupérer les données saisies par l'utilisateur
    brand = request.POST.get('brand')
    min_price = request.POST.get('min_price')
    max_price = request.POST.get('max_price')

    # Filtrer les smartphones en fonction de la marque et de la plage de prix
    filtered_smartphones = smartphones
    if brand:
        filtered_smartphones = [s for s in filtered_smartphones if s['brand'] == brand]
    if min_price:
        filtered_smartphones = [s for s in filtered_smartphones if s['price_final'] >= float(min_price)]
    if max_price:
        filtered_smartphones = [s for s in filtered_smartphones if s['price_final'] <= float(max_price)]

        # Afficher les smartphones filtrés sur une page web
        return render(request, 'skander.html', {'smartphones': filtered_smartphones})

    else:
        return redirect('hello_world')


def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Vérifier si les mots de passe correspondent
        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('create_account')  # Rediriger vers la page de création de compte en cas d'erreur

        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà.")
            return redirect('create_account')  # Rediriger vers la page de création de compte en cas d'erreur

        # Créer un nouvel utilisateur
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Votre compte a été créé avec succès. Vous pouvez vous connecter maintenant.")
        return redirect('login_view')  # Rediriger vers la page de connexion après la création du compte

    return render(request, 'create_account.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def smartphone_price_chart(request):
    smartphones = Smartphone.objects.values('price_final', 'nom').annotate(count=Count('price_final')).order_by(
        'price_final')

    prices = []
    names = []
    counts = []

    for smartphone in smartphones:
        prices.append(smartphone['price_final'])
        names.append(smartphone['nom'])
        counts.append(smartphone['count'])

    plt.bar(prices, counts, label=names)
    plt.xlabel('Price_final')
    plt.ylabel('Count')
    plt.title('Smartphone Price Statistics')
    plt.legend()

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    context = {'smartphone_price': img.read(), 'content_type': 'image/png'}
    return render(request, 'chart.html', context)
