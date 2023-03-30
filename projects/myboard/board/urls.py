# 장고의 기본 라이브러리
from django.urls import path

# 현재 패키지에서 views 를 import하세요
from . import views  # .은 현재 폴더에서 라는 뜻

app_name = 'board'

urlpatterns = [
    # .../board/
    path('', views.index, name='index'),
    path('<int:id>/', views.read, name='detail'),
    path('write/', views.write, name='write'),
    path('<int:id>/update/', views.update, name='update'),
    path('<int:id>/delete/', views.delete, name='delete'),
    # path('search_board/', views.search_board),

    # 댓글 쓰기 주소
    path('<int:id>/write_reply/', views.write_reply, name='write_reply'),
    # 댓글 삭제 주소(id: 글번호, rid: 댓글번호)
    path('<int:id>/delete_reply/<int:rid>/',
         views.delete_reply, name='delete_reply'),

    # 댓글 업데이트 주소
    path('<int:id>/update_reply/', views.update_reply, name='update_reply'),

    # AJAX
    path('callAjax/', views.call_ajax),
    # AJAX_댓글목록
    path('load_reply/', views.load_reply),

    path('<int:id>/load_reply_delete/<int:rid>/',
         views.load_reply_delete, name='load_reply_delete'),

    path('<int:id>/load_update_reply/<int:rid>/',
         views.load_update_reply, name='load_update_reply'),

    path('<int:id>/write_reply/', views.write_reply, name='write_reply'),

]
