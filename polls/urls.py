from django.urls import path

from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('register', views.register, name='register'),
    path('raizes', views.polinomio2, name='raizes'),
    path('Equacao_diofantina', views.equadio, name='equacaodio'),
    path('number', views.number, name='number'),
    path('teoch', views.teoch, name='teoch'),
    path('historic', views.historic, name='historic'),
    path('cadastro', views.cadastro,name='cadastro'),
    path('mudarsenha',views.mudarsenha,name='mudarsenha'),
    path('telainicial', views.telaInicial, name='telaInicial')
]