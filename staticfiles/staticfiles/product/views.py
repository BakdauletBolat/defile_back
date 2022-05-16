from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
from product.models import Brand, Category, Product, ProductFavorites, Type
from rest_framework.views import APIView
from product.serializers import BrandSerializer, CategorySerializer, ProductFavoritesSerializer, ProductSerializer, TypeSerializer
from rest_framework.response import Response
from rest_framework import status
import json


class BrandListApiView(ListAPIView):

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CategoryListApiView(ListAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TypeListApiView(ListAPIView):

    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class ProductListApiView(ListAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['subcategory', 'category','brand','is_new','is_stock','is_hot']


class ProductRetrieveAPIView(RetrieveAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class AddToFavorites(APIView):

    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        post = json.loads(body_unicode)
        print(post)

        if request.user.is_authenticated:

            product_id = post.get('product_id')

            try:
                productFavoriteObject = ProductFavorites.objects.get(
                    owner=request.user, product_id=product_id)
                if productFavoriteObject.is_liked:
                    productFavoriteObject.is_liked = False
                else:
                    productFavoriteObject.is_liked = True

                productFavoriteObject.save()

                productFavorite = ProductFavoritesSerializer(
                    productFavoriteObject).data

                return Response(productFavorite, status=status.HTTP_200_OK)
            except Exception:
                productFavoriteObject = ProductFavorites.objects.create(
                    owner=request.user, product_id=product_id)
                productFavorite = ProductFavoritesSerializer(
                    productFavoriteObject).data

                return Response(productFavorite, status=status.HTTP_200_OK)
        else:
           
            try:
                product_id = post.get('product_id')
                session_id = post.get('session_id')
                try:
                    productFavoriteObject = ProductFavorites.objects.get(
                        session_id=session_id, product_id=product_id)
                    if productFavoriteObject.is_liked:
                        productFavoriteObject.is_liked = False
                    else:
                        productFavoriteObject.is_liked = True

                    productFavoriteObject.save()

                    productFavorite = ProductFavoritesSerializer(
                        productFavoriteObject).data

                    return Response(productFavorite, status=status.HTTP_200_OK)
                except Exception:
                    productFavoriteObject = ProductFavorites.objects.create(
                        session_id=session_id, product_id=product_id)
                    productFavorite = ProductFavoritesSerializer(
                        productFavoriteObject).data

                    return Response(productFavorite, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'message', 'session_id не передано'}, status=status.HTTP_401_UNAUTHORIZED)


class ProductFavoritesListAPIView(APIView):

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            likesDict = []
            for favorite in request.user.likes.filter(is_liked=True):
                print(favorite)
                likesDict.append(favorite.product)
            likes = ProductSerializer(likesDict, many=True,context={'request': request}).data
            return Response(likes, status=status.HTTP_200_OK)
        else:
            try:
                session_id = request.GET.get('session_id')
                likesDict = []
                for favorite in ProductFavorites.objects.filter(
                    session_id=session_id, is_liked=True):
                    print(favorite)
                    likesDict.append(favorite.product)
                likes = ProductSerializer(likesDict, many=True,context={'request': request}).data
                return Response(likes, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'message', 'session_id не передано'}, status=status.HTTP_401_UNAUTHORIZED)
