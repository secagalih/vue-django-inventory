from itertools import product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer
from backend.inventory import serializers
from rest_framework.pagination import PageNumberPagination

# Create your views here.


class ProductPagination(PageNumberPagination):
    pag_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ProductListView(APIView):
    #! GET /api/products/list-items/
    def get(self, request):
        products = Product.objects.all()
        paginator = ProductPagination()
        paginated_products = paginator.paginate_queryset(product, request)
        serializer = ProductSerializer(paginated_products, many=True)
        return Response(serializer.data)


class ProductCreateView(APIView):
    #! POST /api/products/create/

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductUpdateView(APIView):
    # !POST /api/products/<uuid:pk>/update/
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # end def


class ProductDeleteView(APIView):
    # !POST /api/products/<uuid:pk>/delete/
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        deleted_data = serializer.data
        product.delete()
        return Response(
            {
                "message": "Product deleted successfully",
                "deleted_product": deleted_data,
            },
            status=status.HTTP_200_OK,
        )

    # end def
