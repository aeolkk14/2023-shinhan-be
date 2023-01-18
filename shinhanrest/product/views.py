from rest_framework import generics, mixins
from .models import Product

class ProductListView(mixins.ListModelMixin, generics.GenericAPIView): 
    # python 여러 클래스 상속 가능
    # base: generics.GenericAPIView
    # 기능: mixins.ListModelMixin
    
    def get_queryset(self): 
        return Product.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        # Queryset
        # Serialize
        # return Response
        return self.list(request, args, kwargs)