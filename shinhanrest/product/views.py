from rest_framework import generics, mixins
from .models import Product
from .serializers import ProductSerializer
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
        return self.list(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, args, kwargs)