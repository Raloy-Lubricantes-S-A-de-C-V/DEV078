# django
from django.urls import path
from aplications.users import views

urlpatterns = [
    path(
        route='login/',
        view=views.login_view,
        name='login'
    ),

    path(
            route ='logout/',
            view=views.logout_view,
            name='logout'
    ),
]