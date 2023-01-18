from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="회원")
    title = models.CharField(max_length=128, verbose_name='상품명') # max_length: 최대길이
    content = models.TextField(verbose_name='상품내용') # textfield: 길이 지정 x
    price = models.IntegerField(verbose_name='가격')
    location = models.CharField(max_length=256, verbose_name='위치')
    image = models.FileField(null=True, blank=True, verbose_name="이미지") # 중간에 추가했기 때문에 makemigrations, migrate 실행
    # null=True -> db 속성값, blank=True -> py 코드 안에서 null을 안 넣어도 됨, 두개 설정 같이 해야함

    class Meta:
        db_table = 'shinhan_product'
        verbose_name ='상품'
        verbose_name_plural ='상품'

        
