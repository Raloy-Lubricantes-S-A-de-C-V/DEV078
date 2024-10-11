from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def feed_view(request):
     if request.user.is_authenticated:
          print(f"Usuario autenticado: {request.user.username}")
     else:
          print("Usuario no autenticado.")

     return render(request, 'sampling/feed.html', {'ping': 'pong'})