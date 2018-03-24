from django.urls import path

from . import views

urlpatterns = [
    path('', views.signin, name='signin'),
    path('rm/', views.ruumid, name='ruumid'),
    path('postsign/', views.postsign, name='ruumid'),
    path('logout/', views.logout, name='logout'),
    path('uusruum/', views.uusruum, name='uusruum'),
    path('postruum/', views.postruum, name='postruum'),
    path('listruum/', views.listruum, name='listruum'),
    path('uusasi/', views.uusasi, name='uusasi'),
    path('ruumdetails/', views.ruumdetails, name='ruumdetails'),
    path('asidetails/', views.asidetails, name='asidetails'),
    path('ruumedit/', views.ruumedit, name='ruumedit'),
    path('ruumdel/', views.ruumdel, name='ruumdel'),
    path('postasi/', views.postasi, name='postasi'),
    path('listasi/', views.listasi, name='listasi'),
    path('asiedit/', views.asiedit, name='asiedit'),
    path('lisalugu/', views.lisalugu, name='lisalugu'),
    path('postlugu/', views.postlugu, name='postlugu'),
]
