from xmlrpc import client
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Datos de conexión a Odoo
ODOO_URL = 'http://odoo.raloy.com.mx:8069'
ODOO_DB = 'raloy_productivo'

def odoo_authenticate(username, password):

    try:
        common = client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
        uid = common.authenticate(ODOO_DB, username, password, {})
        return uid  # Si es exitoso, retorna el UID del usuario en Odoo
    except Exception as e:
        print(f'Error autenticando contra Odoo: {e}')
        return None

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Autenticar contra Odoo
        odoo_user_id = odoo_authenticate(username, password)

        if odoo_user_id:
            # Si la autenticación en Odoo fue exitosa, verificamos si el usuario existe en Django
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Si no existe, lo creamos
                user = User.objects.create_user(username=username, password=password)

            # Autenticamos localmente en Django (solo con el nombre de usuario)
            user = authenticate(request, username=username, password=password)

            if user:
                # Iniciar sesión en Django
                login(request, user)
                return redirect('sampling:feed')
            else:
                return render(request, 'users/login.html', {'error': 'Error al autenticar localmente en Django'})
        else:
            # Si la autenticación en Odoo falla
            return render(request, 'users/login.html', {'error': 'El usuario o contraseña es invalido'})

    return render(request, 'users/login.html')


@login_required
def logout_view(request):

    logout(request)
    return redirect('users:login')
