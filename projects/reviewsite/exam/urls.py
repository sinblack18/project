from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),

    path('movieadd/', views.movieadd, name='movieadd'),

    path('movieinfo/<int:id>/', views.movieinfo, name='movieinfo'),

    path('movieupdate/<int:id>/', views.movieupdate, name='movieupdate'),

    path('moviedelete/<int:id>/', views.moviedelete, name='moviedelete'),

    path('reviewadd/<int:id>/', views.reviewadd, name='reviewadd'),

    path('orderby_review/', views.orderby_review, name='orderby_review'),

    path('load_review/<int:id>/', views.load_review, name='load_review'),
]
