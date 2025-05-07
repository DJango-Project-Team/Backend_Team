from django.shortcuts import render

from .models import User
from .models import Sign_Up_Users
from django.contrib import messages

def login_view(request): # 여기는 로그인하는 로직을 구현
    #임시로 POST 나중에 GET으로 바꿀예정
    if request.method == 'POST':
        sign_up_id = request.POST.get('sign_up_id')
        sign_up_password = request.POST.get('sign_up_password')
        Sign_Up_Users.objects.get( sign_up_id= sign_up_id, sign_up_password= sign_up_password) #get으로 데이터 베이스를 불러온다.
        return render(request, 'New_Page_01.html')
    return render(request, 'Test_01.html')

#여기 오늘 추가했음. 회원가입 페이지 함수
def sign_up_view(request):
    if request.method == 'POST':
        sign_up_email = request.POST.get('sign_up_email')
        sign_up_password = request.POST.get('sign_up_password')
        sign_up_name = request.POST.get('sign_up_name')
        sign_up_id = request.POST.get('sign_up_id')
        Sign_Up_Users.objects.create(sign_up_email=sign_up_email, sign_up_password=sign_up_password, sign_up_name=sign_up_name, sign_up_id=sign_up_id)
        return render(request, 'success.html')
    return render(request, 'Creat_Acconut.html')

