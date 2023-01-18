from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from .models import Member

# Create your views here.

def login(request):
    if request.method == 'POST':
        user_id=request.POST.get("user_id")
        password=request.POST.get("password")

        if Member.objects.filter(user_id=user_id).exists():
            member = Member.objects.get(user_id=user_id)

            if check_password(password, member.password): # 입력한 비밀번호와 암호화한 비밀번호가 동일한가
                request.session['user_pk'] = member.id
                request.session['user_id'] = member.user_id
                return redirect('/') # 127.0.0.1:8000(상품 페이지)로 넘어감

            # 로그인 성공!

        # 로그인 실패

    return render(request, 'login.html')


def logout(request):
    if 'user_pk' in request.session:
        del(request.session['user_pk'])
    
    if 'user_id' in request.session:
        del(request.session['user_id'])

    return redirect('/')


# 회원가입 페이지 노출
# 회원가입 기능 개발
def register(request):
    if request.method == 'POST':
        user_id=request.POST.get("user_id")
        password=request.POST.get("password")
        name=request.POST.get("name")
        age=request.POST.get("age")

        if not Member.objects.filter(user_id=user_id).exists():
            member = Member(
                user_id=user_id,
                password=make_password(password),
                name=name,
                age=age
            )

            member.save() 
            return redirect('/member/login/') 
    
    return render(request, 'register.html')

    
    