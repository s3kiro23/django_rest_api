from rest_framework import serializers

from shop.models import Category, Product, Article


class CategoryListSerializer(serializers.ModelSerializer):
   
   class Meta:
      model = Category
      fields = ['id', 'date_created', 'date_updated', 'name', 'description']
 
   def validate_name(self, value):
      if Category.objects.filter(name=value).exists():
         raise serializers.ValidationError('Category with this name already exists')
      return value
   
   def validate(self, data):
      if data['name'] not in data['description']:
         raise serializers.ValidationError('Name must be in description')
      return data
   

class CategoryDetailSerializer(serializers.ModelSerializer):
   
   products = serializers.SerializerMethodField()
   
   class Meta:
      model = Category
      fields = ['id', 'date_created', 'date_updated', 'name', 'products']
      
   def get_products(self, instance):
      queryset = instance.products.filter(active=True)
      serializer = ProductDetailSerializer(queryset, many=True)
      return serializer.data
   
   
class ProductListSerializer(serializers.ModelSerializer):
   
   class Meta:
      model = Product
      fields = ['id', 'date_created', 'date_updated', 'name', 'category', 'ecoscore']   
      
   
class ProductDetailSerializer(serializers.ModelSerializer):
   
   articles = serializers.SerializerMethodField()

   class Meta:
      model = Product
      fields = ['id', 'date_created', 'date_updated', 'name', 'category', 'articles']
      
   def get_articles(self, instance):
      queryset = instance.articles.filter(active=True)
      serializer = ArticleSerializer(queryset, many=True)
      return serializer.data
      

class ArticleSerializer(serializers.ModelSerializer):

   class Meta:
      model = Article
      fields = ['id', 'date_created', 'date_updated', 'name', 'price', 'product']
      
   def validate_price(self, value):
      if value < 1:
         raise serializers.ValidationError('Price must be greater than 1 euro')
      return value
   
   def validate_product(self, value):
      if value.active is False:
         raise serializers.ValidationError('Product must be active')
      return value
   
   
   