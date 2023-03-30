from django.urls import path

# 현재 패키지에서 views 를 import하세요
from . import views  # .은 현재 폴더에서 라는 뜻

urlpatterns = [
    # .../order/
    path('', views.index),
    path('order_from/', views.order_from),
    path('search/', views.search_all),
    path('search/<int:id>/', views.order_show),
    path('search_address/', views.search_address),
    path('search/<int:id>/update/', views.update),
    path('search/<int:id>/delete/', views.delete),
]
