from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Member

# Create your views here.

class Register(APIView):
    
    def post(self, request, *args, **kargs):
      
        username=request.data.get('username')
        password=request.data.get('password')
        tel=request.data.get('tel')

        member = Member(
            username=username,
            password=make_password(password),
            tel=tel
        )
   

        member.save()

        return Response(status=status.HTTP_201_CREATED)
