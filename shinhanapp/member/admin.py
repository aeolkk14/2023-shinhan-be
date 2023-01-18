from django.contrib import admin
from .models import Member #. -> 현재 위치의 models 파일

# Register your models here.

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    pass