from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Product, Comment, Like
from .serializers import (
    ProductSerializer, 
    CommentSerializer, 
    CommentCreateSerializer,
    LikeCreateSerializer
)
from .paginations import ProductLargePagination

class ProductListView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin, 
    generics.GenericAPIView
): 
    # python 여러 클래스 상속 가능
    # base: generics.GenericAPIView
    # 기능: mixins.

    serializer_class = ProductSerializer
    pagination_class = ProductLargePagination
    
    
    def get_queryset(self): 
        products = Product.objects.all()

        # if 'name' in self.request.query_params:
        #     name = self.request.query_params['name']
        #     products=products.filter(name__contains=name)

        name=self.request.query_params.get('name')
        if name:
            products=products.filter(name__contains=name)

        return products.order_by('id')

    def get(self, request, *args, **kwargs):
        # Queryset
        # Serialize
        # return Response
        # print(request.user) -> 잘 나오는가
        if request.user.is_authenticated:
            return self.list(request, args, kwargs)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        return self.create(request, args, kwargs)


class ProductDetailView(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView # 내부에 lookup_fild='pk'가 있음
):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by('id') 

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, args, kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, args, kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, args, kwargs) # partial_update: 일부 수정하는 함수


class CommentListView(
    mixins.ListModelMixin,
    generics.GenericAPIView
): 
    serializer_class = CommentSerializer
    # pagination_class는 settings.py에 default로 설정함. 따라서 쓸 필요 없다.

    def get_queryset(self):
        product_id=self.kwargs.get('product_id')
        if product_id:
            return Comment.objects.filter(product_id=product_id).order_by('-id') # product_id == product__pk
        return Comment.objects.none()
    
    def get(self, request, *args, **kwargs):
        return self.list(request, args, kwargs)


class CommentCreateView(
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    serializer_class = CommentCreateSerializer
    
    def get_queryset(self): 
        return Comment.objects.all()
    # 없어도 된다

    def post(self, request, *args, **kwargs):
        return self.create(request, args, kwargs)


class LikeCreateView(
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    serializer_class = LikeCreateSerializer

    # 없어도 된다
    def get_queryset(self):
        return Like.objects.all()

    def post(self, request, *args, **kwargs):
        product_id=request.data.get('product')

        if Like.objects.filter(member=request.user, product_id=product_id).exists():
            Like.objects.filter(member=request.user, product_id=product_id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
       
        return self.create(request, args, kwargs)

