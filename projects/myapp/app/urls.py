# 장고의 기본 라이브러리
from django.urls import path

# 현재 패키지에서 views 를 import하세요
from . import views

urlpatterns =[
    # 해당하는 주소가 입력된다면~
    path('', views.index),
    path('call1',views.call1),
    # 파라미터로 자료형:변수이름이 넘어온다면~
    path('<int:number>/',views.call2),
    path('call3',views.call3),
    path('call4',views.call4),
    path('call5',views.call5),
    path('call6',views.call6),
    path('call_submit',views.call_submit),
]