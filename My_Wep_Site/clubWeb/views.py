from django.shortcuts import render, get_object_or_404, redirect
from .models import Club, Application
from .forms import ApplicationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache, cache_control
from functools import wraps
from django.contrib import messages

# 로그인 했고 로그인 하지 않았을 때를 구별 하는  뷰(추가 된 뷰)
def check_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('/sign/login/')
        return view_func(request, *args, **kwargs)
    return wrapper

# 동아리 목록 페이지
def main_view(request):
    # DB에서 모든 동아리 정보 가져오기
    clubs = Club.objects.all()  # club_main 테이블에서 모든 동아리 정보 가져오기
    return render(request, 'club/main.html', {'clubs': clubs})

# 동아리 상세 페이지
def club_detail(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    return render(request, 'club/club_detail.html', {'club': club})

# 신청서 페이지
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
@check_login_required
def application_form(request, club_id):
    club = get_object_or_404(Club, pk=club_id)

    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            student_id = request.session.get('student_id')
            student_name = request.session.get('student_name')

            # 이미 신청한 경우 체크함 ( 신청할때 id값을 따로 저장하는데, 유효한 id이력이 있으면 제출이 안되고 아래 메세지를 출력 )
            if Application.objects.filter(club=club, student_id=student_id).exists():
                messages.warning(request, "이미 신청하셨습니다.")
                return redirect('club_detail', club_id=club_id)

            application = form.save(commit=False)
            application.club = club
            application.student_id = student_id
            application.student_name = student_name
            application.save()

            return redirect('application_success')
    else:
        form = ApplicationForm()

    return render(request, 'club/application_form.html', {'form': form, 'club': club})

# 신청 완료 페이지
def application_success(request):
    return render(request, 'club/application_success.html')

# 로그아웃 뷰
def logout_view(request):
    request.session.flush()
    return redirect('main_view')

# 동아리 신청 목록에 어떤 동아리 신청했나 확인하는 뷰
@check_login_required
def my_applications_view(request):
    student_id = request.session.get('student_id')  # 로그인한 사용자 식별
    club_name = request.GET.get('club_name')  # 선택된 동아리 필터

    if club_name:
        applications = Application.objects.filter(student_id=student_id, club__name=club_name)
    else:
        applications = Application.objects.filter(student_id=student_id)

    clubs = Club.objects.all()
    return render(request, 'club/club_application_site.html', {
        'applications': applications,
        'clubs': clubs,
    })

# 수정 시 오류 안되게 하는 코드? (수정요망?? 근데 이거 없으면 안됌)
@check_login_required
def edit_application_view(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('application_edit_success')  # 수정 후 목록으로 이동
    else:
        form = ApplicationForm(instance=application)  # 기존 데이터를 폼에 채워넣음

        return render(request, 'club/application_edit_form.html', {
            'form': form,
            'application': application
        })

# 신청서를 수정하는 뷰
@check_login_required
def application_edit(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    if request.method == "POST":
        form = ApplicationForm(request.POST, instance=application)  # 기존 데이터를 수정
        if form.is_valid():
            form.instance.student_id = application.student_id
            form.save()  # 수정 정보를 저장
            return redirect('application_edit_success')  # 성공 시 보여줌
    else:
        form = ApplicationForm(instance=application)  # 기존 내용이 채워진 폼

    return render(request, 'club/application_edit_form.html', {'form': form})

# 신청한 선청서를 삭제하는 뷰
@check_login_required
def delete_application_view(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    # 요청 방식이 POST인 경우에만 삭제
    if request.method == "POST":
        application.delete()
        return redirect('my_applications_view')  # 삭제 후 목록으로 이동

    # GET으로 삭제 요청이 오면 비정상 처리 (선택 사항)
    return redirect('my_applications_view')

# 신청서를 수정 성공 시 나오는 뷰
def application_edit_success(request):
    return render(request, 'club/application_edit_success.html')