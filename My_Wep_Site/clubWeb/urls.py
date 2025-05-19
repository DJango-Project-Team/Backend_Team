from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main_view'),  # 동아리 목록 페이지
    path('club/<int:club_id>/', views.club_detail, name='club_detail'),  # 동아리 상세 페이지
    path('club/<int:club_id>/apply/', views.application_form, name='application_form'),  # 신청 폼 페이지
    path('application_success/', views.application_success, name='application_success'),# 신청 완료 페이지
    path('logout/', views.logout_view, name='logout'), #로그아웃 뷰

    #여기서 부터 추가 된 url

    path('application_inventory/', views.my_applications_view, name='application_inventory'), # 신청서 저장소
    path('application/<int:application_id>/edit/', views.edit_application_view, name='edit_application'), # 신청서 수정
    path('application_edit_success/', views.application_edit_success, name='application_edit_success'), # 신청서 수정 성공 뷰
    path('application/<int:application_id>/edit/', views.application_edit, name='application_edit'), # 수정 페이지로 가는 뷰
    path('my_applications/', views.my_applications_view, name='my_applications_view'), # 수정을 눌렀을 때 오류를 해결하는 뷰
    path('application/<int:application_id>/delete/', views.delete_application_view, name='delete_application'), # 삭제를 눌렀을때 신청서 삭제


]

