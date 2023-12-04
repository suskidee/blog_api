from django.core.paginator import Paginator
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import BlogSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Blog
from django.db.models import Q


class PublicBlogView(APIView):
    def get(self, request):
        try:

            blogs = Blog.objects.all().order_by("?")

            if request.GET.get("search"):
                search = request.GET.get("search")
                blogs = Blog.objects.filter(Q(title__icontains=search) | Q(blog_text__icontains=search))

            page_number = request.GET.get('page', 1)
            paginator = Paginator(blogs, 10)
            serializer = BlogSerializer(paginator.page(page_number), many=True)

            return Response({
                'data': serializer.data,
                'message': "blogs fetched successfully"
            }, status=HTTP_200_OK)

        except Exception as e:
            return Response({
                'data': {},
                'message': "invalid page number"
            }, status=HTTP_400_BAD_REQUEST)

class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            blogs = Blog.objects.filter(user=request.user)

            if request.GET.get("search"):
                search = request.GET.get("search")
                blogs = Blog.objects.filter(Q(title__icontains=search) | Q(blog_text__icontains=search))

            serializer = BlogSerializer(blogs, many=True)
            return Response({
                'data': serializer.data,
                'message': "blogs fetched successfully"
            }, status=HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({
                'data': serializer.errors,
                'message': "something went wrong ooo"
            }, status=HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            data = request.data
            data["user"] = request.user.id
            serializer = BlogSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': "something went wrong"
                }, status=HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                'data': serializer.data,
                'message': "blog created successfully"
            }, status=HTTP_200_OK)

        except Exception as e:
            return Response({
                'data': {},
                'message': "something went wrong ooo"
            }, status=HTTP_400_BAD_REQUEST)

    def patch(self,request):
        try:
            data = request.data

            blog = Blog.objects.filter(uid=data.get("uid"))
            if not blog.exists():
                return Response({
                    'data': {},
                    'message': "invalid blog uid"
                }, status=HTTP_400_BAD_REQUEST)

            if request.user != blog[0].user:
                return Response({
                    'data': {},
                    'message': "you are not authorized to do this"
                }, status=HTTP_400_BAD_REQUEST)

            serializer = BlogSerializer(blog[0], data=data, partial=True)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': "something went wrong. data input invalid"
                }, status=HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                'data': serializer.data,
                'message': "blog updated successfully"
            }, status=HTTP_200_OK)

        except Exception as e:
            return Response({
                'data': {},
                'message': "something went wrong during serialization"
            }, status=HTTP_400_BAD_REQUEST)

    def delete(self,request):
        try:
            data = request.data

            blog = Blog.objects.filter(uid=data.get("uid"))
            if not blog.exists():
                return Response({
                    'data': {},
                    'message': "invalid blog uid"
                }, status=HTTP_400_BAD_REQUEST)

            if request.user != blog[0].user:
                return Response({
                    'data': {},
                    'message': "you are not authorized to do this"
                }, status=HTTP_400_BAD_REQUEST)

            blog[0].delete()
            return Response({
                'data': {},
                'message': "blog deleted successfully"
            }, status=HTTP_200_OK)

        except Exception as e:
            return Response({
                'data': {},
                'message': "something went wrong during serialization"
            }, status=HTTP_400_BAD_REQUEST)