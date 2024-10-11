from xmlrpc import client
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Datos de conexión a Odoo
ODOO_URL = 'http://odoo.raloy.com.mx:8069'
ODOO_DB = 'raloy_productivo'
ODOO_ADMIN_USERNAME = 'cgarcia@raloy.com.mx'
ODOO_ADMIN_PASSWORD = 'gr101320'

def odoo_authenticate(login, password):
    try:
        common = client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
        uid = common.authenticate(ODOO_DB, login, password, {})
        return uid
    except Exception as e:
        print(f'Error autenticando contra Odoo: {e}')
        return None


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('sampling:feed')
        else:
            return render(request, 'users/login.html', {'error': 'El usuario o contraseña es invalido'})

    return render(request, 'users/login.html')


@login_required
def logout_view(request):

    logout(request)
    return redirect('users:login')
