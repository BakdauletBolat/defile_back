from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from product.models import ProductFavorites
from users.serializers import UserCreateSerializer
from .models import Order, OrderItem
from .serializers import OrderSerializer
from users.models import CustomUser
from operator import itemgetter
from passwordgenerator import pwgenerator
from rest_framework_simplejwt.tokens import RefreshToken
from store.serializers import OrderSerializer
from store.models import Order
from rest_framework.permissions import IsAuthenticated

# Create your views here.
import json


def get_tokens_for_user(user, data):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': data,
    }


class OrderListApiView(ListAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(self.queryset)
        return self.queryset.filter(owner=self.request.user)


class GetOrderToUser(APIView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                basket = Order.objects.get(owner=request.user, status='ожидает')
                print(basket)
                return JsonResponse(OrderSerializer(basket, context={'request': request}).data)

            except Exception as e:
                print(e)
                basket = Order.objects.create(owner=request.user)
                return JsonResponse(OrderSerializer(basket, context={'request': request}).data)
        else:
            session = request.GET.get('session_id')
            try:
                basket = Order.objects.get(session_id=session, status='ожидает')
                print(basket)
                return JsonResponse(OrderSerializer(basket, context={'request': request}).data)

            except Exception as e:
                print(e)
                basket = Order.objects.create(session_id=session)
                return JsonResponse(OrderSerializer(basket, context={'request': request}).data)


class CreateOrderUnauthorizedUser(APIView):

    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        post = json.loads(body_unicode)

        email, phone, fullname, session_id = itemgetter(
            'email', 'phone', 'fullname', 'session_id')(post)
        password = pwgenerator.generate()

        def fromSessionToCustomUser(session_id,user_id):
            try:
                favObjects = ProductFavorites.objects.filter(session_id=session_id)
                for favObject in favObjects:
                    favObject.owner_id = user_id
                    favObject.save()

            except Exception:
                print('нет данных')
            

        try:
            order = Order.objects.get(session_id=session_id, status='ожидает')
            user = None
            try:
                user = CustomUser.objects.create_user(email, password,phone,fullname)
            except Exception as e:
                print(e)
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            order.owner = user
            order.status = 'принят'
            order.save()
            fromSessionToCustomUser(session_id,user.id)
            serializer = UserCreateSerializer(user)
            data = get_tokens_for_user(user, serializer.data)
            return Response(data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateOrderAuthorizedUser(APIView):

    def post(self, request, *args, **kwargs):
        print(request.user)
        try:
            order = Order.objects.get(owner=request.user, status='ожидает')
            order.status = 'принят'
            order.save()
            return Response({
                'message': 'Успешно принят заказ'
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AddProductToBasket(APIView):

    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        post = json.loads(body_unicode)
        product_id = post.get('product_id')
        qty = post.get('qty')
        if request.user.is_authenticated:
            try:
                basket = Order.objects.get(
                    owner=request.user, status='ожидает')
                OrderItem.objects.create(
                    product_id=product_id, order=basket, qty=qty)
                return JsonResponse({'message': 'Успешно добавлено', 'statusCode': 201})
            except Exception:
                basket = Order.objects.create(owner=request.user)
                OrderItem.objects.create(
                    product_id=product_id, order=basket, qty=qty)

                return JsonResponse({'message': 'Успешно добавлено', 'statusCode': 200})
        else:
            session_id = post.get('session_id')
            try:
                basket = Order.objects.get(
                    session_id=session_id, status='ожидает')
                OrderItem.objects.create(
                    product_id=product_id, order=basket, qty=qty)
                return JsonResponse({'message': 'Успешно добавлено', 'statusCode': 201})
            except Exception:
                basket = Order.objects.create(session_id=session_id)
                OrderItem.objects.create(
                    product_id=product_id, order=basket, qty=qty)
                return JsonResponse({'message': 'Успешно добавлено', 'statusCode': 200})



class OrderQtyUpdateView(APIView):

    def post(self,request):
        body_unicode = request.body.decode('utf-8')
        post = json.loads(body_unicode)

        order_id = post['order_id']
        type = post['type']


        order = get_object_or_404(OrderItem,id=order_id)

        if type == 'add':
            order.qty += 1
        elif type == 'remove':
            order.qty -= 1
        
        order.save()

        return Response({'message':f'updated orderItem - {order_id}' },status=status.HTTP_200_OK)
        


class OrderResultAPIView(APIView):

    def post(self,request):
        print('hello')
        print(request)
        return JsonResponse('hey')

    def get(self,request):
        print('hello')
        print(request)

        return JsonResponse('hey')
