from django.shortcuts import render
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer,LoginSerializer


# Create your views here.


class RegisterView(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': "something went wrong"
                }, status=HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                'data': {},
                'message': "your account is created"
            }, status=HTTP_200_OK)

        except Exception as e:
            return Response({
                'data': serializer.errors,
                'message': "something went wrong ooo"
            }, status=HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': "something went wrong"
                }, status=HTTP_400_BAD_REQUEST)

            response = serializer.get_jwt_token(serializer.data)
            return Response(response, status=HTTP_200_OK)

        except Exception as e:
            return Response({
                'data': serializer.errors,
                'message': "something went wrong ooo"
            }, status=HTTP_400_BAD_REQUEST)