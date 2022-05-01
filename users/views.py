from django.shortcuts import render
from rest_framework import generics
from users.models import CustomUser
from rest_framework import status
from rest_framework.response import Response
from users.serializers import UserCreateSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

def get_tokens_for_user(user,data):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': data,
    }


class RegisterUserView(generics.CreateAPIView):

    serializer_class = UserCreateSerializer
    queryset = CustomUser.objects.all()

    def perform_create(self, serializer):
        return serializer.save()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        data = get_tokens_for_user(user,serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

class GetUser(APIView):

    def get(self,request):

        if request.user.is_authenticated:
            return Response(UserCreateSerializer(request.user).data,status=status.HTTP_200_OK)
        else:
            return Response({'message':'user ist auth'},status=status.HTTP_401_UNAUTHORIZED)
    