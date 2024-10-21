from xmlrpc import client
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from aplications.users.models import Profile

# Datos de conexión a Odoo
ODOO_URL = 'http://odoo.raloy.com.mx:8069'
ODOO_DB = 'raloy_productivo'


def odoo_authenticate(username, password):
    """
    Autentica contra Odoo usando XML-RPC. Retorna el UID si la autenticación es exitosa, o None si falla.
    """
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

        # Autenticar contra Odoo
        odoo_user_id = odoo_authenticate(username, password)

        if odoo_user_id:
            try:
                # Verificar si el usuario ya existe en Django
                user = User.objects.get(username=username)
                # Si el usuario existe, actualizamos su contraseña en Django para que coincida con la de Odoo
                user.set_password(password)
                user.save()
            except User.DoesNotExist:
                # Si no existe, lo creamos junto con el perfil
                user = User.objects.create_user(username=username, password=password)
                Profile.objects.create(user=user)

            # Autenticar localmente en Django con la nueva contraseña
            user = authenticate(request, username=username, password=password)

            if user:
                # Iniciar sesión en Django
                login(request, user)
                return redirect('sampling:feed')
            else:
                return render(request, 'users/login.html', {'error': 'Error al autenticar localmente en Django'})
        else:
            return render(request, 'users/login.html', {'error': 'El usuario o contraseña es inválido'})

    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('users:login')
