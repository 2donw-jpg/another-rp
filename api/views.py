from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from zybal.models import Profile, Post, Notification
from api.serializers import ProfileMainSerializer, PostMainSerializer, NotificationSerializer
from dev import settings
import os

class ProfileListAPIView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileMainSerializer
    pagination_class = PageNumberPagination  

class ProfileAPIView(APIView):
    
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
    queryset = Post.objects.all()
    serializer_class = PostMainSerializer
    pagination_class = PageNumberPagination  

class PostAPIView(APIView):    
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostMainSerializer(post)
        return Response(serializer.data)

class NotificationAPIView(APIView):
    def get(self, request, username):
        notifications = Notification.objects.filter(user__user__username=username)
        paginator = PageNumberPagination()
        paginator.page_size = 2  
        result_page = paginator.paginate_queryset(notifications, request)
        serializer = NotificationSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
