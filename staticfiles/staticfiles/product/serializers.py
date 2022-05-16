from unicodedata import category
from .models import Product,Brand,Category, ProductFavorites, ProductImage, SubCategory,Type
from rest_framework import serializers



class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = ('__all__')

class CategorySerializer(serializers.ModelSerializer):

    subcategorires = SubCategorySerializer(read_only=True,many=True)

    class Meta:
        model = Category
        fields = ('__all__')


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ('__all__')


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('__all__')


class ProductFavoritesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductFavorites
        fields = ('__all__')

class ProductSerializer(serializers.ModelSerializer):

    images = ProductImageSerializer(many=True,read_only=True)
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    likes = serializers.SerializerMethodField()

    def get_likes(self,queryset):
        objectQ = queryset.likes.filter(is_liked=True)

        return ProductFavoritesSerializer(objectQ,many=True).data

    class Meta:
        model = Product
        fields = ('__all__')







class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ('__all__')


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ('__all__')