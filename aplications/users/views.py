from xmlrpc import client
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Datos de conexión a Odoo
ODOO_URL = 'http://odoo.raloy.com.mx:8069'
ODOO_DB = 'raloy_productivo'


def odoo_authenticate(username, password):
    try:
        common = client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
        uid = common.authenticate(ODOO_DB, username, password, {})
        return uid
    except Exception as e:
        print(f'Error autenticando contra Odoo: {e}')
        return None


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        odoo_user_id = odoo_authenticate(username, password)

        if odoo_user_id:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(username=username, password=password)
            user = authenticate(request, username=username, password=password)

            # Iniciar sesión en Django
            if user:
                login(request, user)
                return redirect('sampling:feed')
            else:
                return render(request, 'users/login.html', {'error': 'Error al autenticar localmente en Django'})
        else:
            return render(request, 'users/login.html', {'error': 'El usuario o contraseña es invalido'})

    return render(request, 'users/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('users:login')
