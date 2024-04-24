from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from zybal.models import Profile, Post, Notification
from api.serializers import ProfileMainSerializer, PostMainSerializer, NotificationSerializer, PostUploadSerializer
from dev import settings
import os

class ProfileListAPIView(ListAPIView):
    '''authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]'''
    queryset = Profile.objects.all()
    serializer_class = ProfileMainSerializer
    pagination_class = PageNumberPagination  

class ProfileAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, username):
        profile = get_object_or_404(Profile, user__username=username)
        serializer = ProfileMainSerializer(profile)

        return Response(serializer.data)      

    def put(self, request, username):
        profile = get_object_or_404(Profile, user__username=username)
        serializer = ProfileMainSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListAPIView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostMainSerializer()
    pagination_class = PageNumberPagination  

class PostAPIView(APIView):  
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostMainSerializer(post)
        return Response(serializer.data)

class NotificationAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, username):
        notifications = Notification.objects.filter(user__user__username=username)
        paginator = PageNumberPagination()
        paginator.page_size = 2  
        result_page = paginator.paginate_queryset(notifications, request)
        serializer = NotificationSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


""" class AdminAuthTokenView(APIView):
    def post(self, request, *args, **kwargs):
        # Obtener el usuario de administrador
        admin_user = User.objects.get(username='tu_nombre_de_usuario_de_administrador')
        # Crear o obtener un token para el usuario de administrador
        token, created = Token.objects.get_or_create(user=admin_user)
        return Response({'token': token.key})
         """
