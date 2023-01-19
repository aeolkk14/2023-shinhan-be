from django.contrib.auth.hashers import check_password
from .models import Member

class MemberAuth:

    # 인증 백엔드에 꼭 필요한 함수 2개 -> authenticat, get_user
    def authenticate(self, request, username=None, password=None, *args, **kwargs):
        # username=kwargs.get('username') <- username=None 을 안 쓰면
        # password=kwargs.get('password') <- password=None 을 안 쓰면
        
        if not username or not password:
            if request.user.is_authenticated: # 로그인 되어 있다면
                return request.user 
            return None # 로그인 실패


        try:
            member=Member.objects.get(username=username)
        except Member.DoesNotExist:
            return None

        if check_password(password, member.password):
            if member.status == '일반':
                return member # 로그인 성공

        return None

    def get_user(self, pk): # 사용자를 받아오는 함수
        try:
            member=Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            return None
        
        return member # if member.is_active and member.status=='일반' else None