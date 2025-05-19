from django.shortcuts import render, redirect
from .models import User
from .models import Sign_Up_Users
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        sign_up_password = request.POST.get('sign_up_password')

        try:
            if '@' in user_input:
                user = Sign_Up_Users.objects.get(sign_up_email=user_input, sign_up_password=sign_up_password)
            else:
                user = Sign_Up_Users.objects.get(sign_up_id=user_input, sign_up_password=sign_up_password)
            # 세션에  저장
            request.session['user_id'] = user.id
            request.session['user_name'] = user.sign_up_name
            request.session['student_id'] = user.sign_up_id
            request.session['student_name'] = user.sign_up_name

            from clubWeb.models import Club
            clubs = Club.objects.all()
            return redirect('main_view')

        except Sign_Up_Users.DoesNotExist:
            messages.error(request, "아이디 혹은 비밀번호가 일치하지 않습니다.")
            return redirect('login')

    return render(request, 'sign/Test_01.html')



#여기 오늘 추가했음. 회원가입 페이지 함수
def sign_up_view(request):
    if request.method == 'POST':
        sign_up_email = request.POST.get('sign_up_email')
        sign_up_password = request.POST.get('sign_up_password')
        sign_up_name = request.POST.get('sign_up_name')
        sign_up_id = request.POST.get('sign_up_id')

        email_exists = Sign_Up_Users.objects.filter(sign_up_email=sign_up_email).exists()
        id_exists = Sign_Up_Users.objects.filter(sign_up_id=sign_up_id).exists()

        # 중복 검사: 이메일과 아이디가 이미 존재하는지 확인
        if id_exists and email_exists:
            messages.error(request, "아이디와 이메일이 모두 이미 사용 중입니다.")
            return render(request, 'sign/Creat_Acconut.html')
        elif id_exists:
            messages.error(request, "이미 사용 중인 아이디입니다.")
            return render(request, 'sign/Creat_Acconut.html')
        elif email_exists:
            messages.error(request, "이미 사용 중인 이메일입니다.")
            return render(request, 'sign/Creat_Acconut.html')

        try:
            # 유저 생성
            Sign_Up_Users.objects.create(
                sign_up_email=sign_up_email,
                sign_up_password=sign_up_password,
                sign_up_name=sign_up_name,
                sign_up_id=sign_up_id
            )
            return render(request, 'sign/success.html')
        except Exception as e:
            messages.error(request, f"회원가입 중 오류가 발생했습니다: {str(e)}")
            return render(request, 'sign/Creat_Acconut.html')

    return render(request, 'sign/Creat_Acconut.html')

