from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),

    path('iteminfo/', views.iteminfo, name='iteminfo'),

    path('orderinfo/', views.orderinfo, name='orderinfo'),

    path('itemadd/', views.itemadd, name='itemadd'),

    path('itemupdate/<int:id>/', views.itemupdate, name='itemupdate'),

    path('itemdelete/<int:id>/', views.itemdelete, name='itemdelete'),

    path('orderadd/', views.orderadd, name='orderadd'),

    path('orderupdate/<int:id>/', views.orderupdate, name='orderupdate'),

    path('orderdelete/<int:id>/', views.orderdelete, name='orderdelete'),
]
