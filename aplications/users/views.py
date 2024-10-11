from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('sampling:feed')  # Utilizamos el nombre de la url
        else:
            return render(request, 'users/login.html', {'error': 'El usuario es invalido'})

    return render(request, 'users/login.html')
