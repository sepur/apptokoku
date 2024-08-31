from django.urls import path

from . import views

urlpatterns = [
    path('coba-api/', views.coba_api, name='coba-api'),
    path('add-beli/', views.addbeli, name='add-beli'),
    path('bayar/', views.bayar, name='bayar'),
    path('print-rinci/<int:objects_id>/', views.print_rinci, name='print-rinci'),
    path('addstok-barang/', views.addstok_barang, name='addstok-barang'),
    path('autokomplit/', views.autokomplit, name='autokomplit'),
    path('memberautokomplit/', views.memberautokomplit, name='memberautokomplit'),
    path('eksekusi-stok/', views.eksekusi_stok, name='eksekusi-stok'),
    path('add-barang/', views.add_barang, name='add-barang'),
    path('daftar-kasbon/', views.daftar_kasbon, name='daftar-kasbon'),

]
