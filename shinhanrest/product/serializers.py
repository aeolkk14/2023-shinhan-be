from rest_framework import serializers
from .models import Product, Comment, Like


class ProductSerializer(serializers.ModelSerializer):
    comment_count=serializers.SerializerMethodField()

    def get_comment_count(self, obj): # obj -> Product
        return obj.comment_set.all().count()
        # return Comment.objects.filter(product=obj).count()

    class Meta:
        model = Product
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    member_username = serializers.SerializerMethodField()
    tstamp = serializers.DateTimeField(
        read_only=True, format='%Y-%m-%d %H:%M:%S' 
    )

    def get_product_name(self, obj):
        return obj.product.name

    def get_member_username(self, obj):
        return obj.member.username

    class Meta:
        model = Comment
        fields = "__all__"

class CommentCreateSerializer(serializers.ModelSerializer):
    member=serializers.HiddenField( # member 숨김
        default=serializers.CurrentUserDefault(), 
        required=False
    )
    # def validate(self, attrs):
    #     request=self.context['request'] # request 객체 없음. view.py에 먼저 선언하고 request 가능
    #     if request.user.is_authenticated:
    #         attrs['member']=request.user
    #     else:
    #         raise ValidationError('member is required.')

    #     return attrs

    def validate_member(self, value):
        if not value.is_authenticated:
            raise serializers.ValidationError('member is required')
        return value

    class Meta:
        model=Comment
        fields="__all__"
        # extra_kwargs={'member': {'required':False}}

class LikeCreateSerializer(serializers.ModelSerializer):

    # 멤버를 자동으로 넣겠다
    member=serializers.HiddenField( 
        default=serializers.CurrentUserDefault(), 
        required=False
    )

    # member에 대한 유효성 검사 함수
    # value = request.user
    def validate_member(self, value):
        if not value.is_authenticated:
            raise serializers.ValidationError('member is required')
        return value

    class Meta:
        model=Like
        fields="__all__"
        