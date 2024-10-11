from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def feed_view(request, *args, **kwargs):
     return render(request, 'sampling/feed.html',{'ping':'pong'})