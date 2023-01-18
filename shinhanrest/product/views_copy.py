from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product


class ProductListView(APIView):
    def post(self, request, *args, **kargs):
        # if request.method == 'POST': -> 안 써도 됨
        product=Product(
            name=request.data.get('name'), # 데이터를 가져올 때 data라고 일관되게 쓰기
            price=request.data.get('price'),
            product_type=request.data.get('product_type'),
        )
        # 전달한 값 받아오기
        # Product 객체 생성

        product.save() # db에 저장, primary key가 이때 만들어짐

        return Response({
            'id': product.id, 
            'name': product.name,
            'price': product.price,
            'product_type': product.product_type,
        }, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kargs):
        ret=[]
        products=Product.objects.all() # 이 순간 DB에서 가져오지 않음

        if 'price' in request.query_params:
            price = request.query_params['price']
            products = products.filter(price__lte=price) # price__lte: price보다 작거나 같은

        if 'name' in request.query_params:
            name = request.query_params['name']
            products = products.filter(name__contains=name)

        products = products.order_by('id') # 이 순간 DB에서 가져오지 않음

        for product in products:
            p={
                'id': product.id, # 이때 가져옴
                'name': product.name,
                'price': product.price,
                'product_type': product.product_type,
            }
            ret.append(p)
        
        return Response(ret)


class ProductDetailView(APIView):
    def put(self, request, pk, *args, **kargs):
        product=Product.objects.get(pk=pk) # Product 객체 가져옴

        # if 'name' in request.data:
        #     product.name=request.data['name']
        
        # if 'price' in request.data:
        #     product.price=request.data['price']
        
        # if 'product_type' in request.data:
        #     product.product_type=request.data['product_type']

        dirty = False # 수정된 값이 있는가 -> False: 없음, True: 있음

        for field, value in request.data.items(): # 하나라도 다른게 있으면 dirty = True 가 되는 코드
            if field not in [f.name for f in product._meta.get_fields()]:
                continue
            
            dirty = dirty or (value != getattr(product, field))
            # (value != getattr(product, field)) -> 원래 값이랑 수정한 값이랑 다르면 -> False of True = True -> dirty = True
            setattr(product, field, value)        
        
        if dirty: # 바뀐게 있을 때 (dirty = True)
            product.save()
        # 수정이 됐을 때만 세이브하기 위한 코드 (56-63)

        return Response()
        
        

    def delete(self, request, pk, *args, **kargs):
        # 1. 없으면 지워졌다고 거짓말 하기 (204 반환) -> 이거로 작성
        # 2. 없으면 없다고 반환하기 (404 반환)
        
        if Product.objects.filter(pk=pk).exists():
            product=Product.objects.get(pk=pk) # 삭제할거 가져오기
            product.delete() # 가져온거 삭제

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, *args, **kargs):
        # 1. get 하기 전에 exists()로 확인하고 가져오기
        # 2. get 할 때 예외처리 하기 -> 이거로 작성

        try:        
            product=Product.objects.get(pk=pk) 
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        ret={
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'product_type': product.product_type,
        }
        
        return Response(ret)