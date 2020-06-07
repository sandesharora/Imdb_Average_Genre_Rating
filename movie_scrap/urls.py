from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movie', views.movie, name='movie'),
    path('Genre',views.Genre,name='Genre')

]