from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# 장고가 제공하는 기본 회원가입 폼
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# 우리가 만든 커스텀 회원가입 폼
from .forms import UserForm, CustomchangeForm

# Create your views here.


def index(request):

    return render(request, 'common/index.html')


def signup(request):

    if request.method == 'POST':
        # 요청 객체가 담고있는 정보는 사용자 생성 폼 만든다
        print(request.POST)
        form = UserCreationForm(request.POST)

        if form.is_valid():  # form의 내용이 유효하다면
            form.save()  # db에 폼 정보 저장

            username = form.cleaned_data.get('username')  # 폼에 입력한 값 가져오기
            raw_password = form.cleaned_data.get('password1')

            # 사용자 인증
            user = authenticate(username=username, password=raw_password)
            # 로그인
            login(request, user)

            return redirect('/')

    else:
        # GET 방식으로 요청이 오면 비어있는 사용자 생성 폼을 만든다
        form = UserCreationForm()

    return render(request, 'common/signup.html', {'form': form})


def signup_custom(request):
    if request.method == 'POST':
        print(request.POST)  # QueryDict 한번 보기

        # request.POST에 들어 있는 정보를 UserForm 형식으로 변환
        form = UserForm(request.POST)

        print(form)

        # form이 유효한가?
        if form.is_valid():
            form.save()  # 폼의 내용을 DB(auth_user)에 바로 저장

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            # 사용자 인증 후 로그인
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('/')  # 로그인 하고 메인 페이지로 넘김

    else:
        form = UserForm()  # 새 폼 만들어 주기

    return render(request, 'common/signup.html', {'form': form})


def delete(request):

    if request.user.is_authenticated:
        request.user.delete()  # user 정보 삭제

        # render나 redirect의 파라미터로 app_name:url_name 작성 가능
        return redirect('common:index')


def update(request):

    if request.method == 'POST':
        # instance로 유저 정보 불러옴 그리고 포스트로 불러온걸 위에다가 덮음
        form = CustomchangeForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()  # 폼이 유효하다면 해당 내용 저장
            return redirect('common:index')
    else:
        # CustomchangeForm(instance) 보내면 django가 제공하는 기본 폼 사용할 수 있음
        form = CustomchangeForm(instance=request.user)

    return render(request, 'common/update.html', {'form': form})


def showinfo(request):

    return render(request, 'common/showinfo.html')
