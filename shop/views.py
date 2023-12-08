from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from shop.permissions import IsAdminAuthenticated, IsStaffAuthenticated

from shop.models import Category, Product, Article
from shop.serializers import CategoryDetailSerializer, CategoryListSerializer, ProductListSerializer, ProductDetailSerializer, ArticleSerializer


class MultipleSerializersMixin:
   
   detail_serializer_class = None
   
   def get_serializer_class(self):
      if self.action == 'retrieve' and self.detail_serializer_class is not None:
         return self.detail_serializer_class
      return super().get_serializer_class()
   

class CategoryViewset(MultipleSerializersMixin, ReadOnlyModelViewSet):
   
   serializer_class = CategoryListSerializer
   detail_serializer_class = CategoryDetailSerializer
   
   @action(detail=True, methods=['post'])
   def disable(self, request, pk):
      self.get_object().disable()
      return Response()
   
   def get_queryset(self):
      return Category.objects.filter(active=True)
   
   
class ProductViewset(MultipleSerializersMixin, ReadOnlyModelViewSet):
   
   serializer_class = ProductListSerializer
   detail_serializer_class = ProductDetailSerializer
   
   @action(detail=True, methods=['post'])
   def disable(self, request, pk):
      self.get_object().disable()
      return Response()
   
   def get_queryset(self):
      queryset =  Product.objects.filter(active=True)
      
      category_id = self.request.GET.get('category_id')
      if category_id is not None:
         queryset = queryset.filter(category_id=category_id)
      return queryset
   
   
class ArticleViewset(ReadOnlyModelViewSet):
   
   serializer_class = ArticleSerializer
   
   def get_queryset(self):
      queryset = Article.objects.filter(active=True)
      
      product_id = self.request.GET.get('product_id')
      if product_id is not None:
         queryset = queryset.filter(product_id=product_id)
      return queryset
   
   
class AdminCategoryViewset(MultipleSerializersMixin, ModelViewSet):
   
   serializer_class = CategoryListSerializer
   detail_serializer_class = CategoryDetailSerializer
   permission_classes = [IsAdminAuthenticated, IsStaffAuthenticated]
   
   def get_queryset(self):
      return Category.objects.all()
   
   
class AdminArticleViewset(MultipleSerializersMixin, ModelViewSet):
   
   serializer_class = ArticleSerializer
   
   def get_queryset(self):
      return Article.objects.all()