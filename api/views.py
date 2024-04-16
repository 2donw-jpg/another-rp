from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from zybal.models import Profile, Post, Notification
from api.serializers import ProfileSerializer, PostSerializer, NotificationSerializer
from dev import settings
import os

class ProfileListAPIView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileAPIView(APIView):
    
    """def get(self, request, id_user):
        try:
            profile = Profile.objects.get(user__id=id_user)
            profile_serializer = ProfileSerializer(profile)
            posts = Post.objects.filter(user__id=id_user)
            post_serializer = PostSerializer(posts, many=True)
            return Response({
                "profile": profile_serializer.data,
                "posts": post_serializer.data
            })
        except Profile.DoesNotExist:
            return Response({"error": "Profile does not exist"}, status=status.HTTP_404_NOT_FOUND)"""
    
    def get(self, request, id_user):
        profile = get_object_or_404(Profile, user__id=id_user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)      

    def put(self, request, user_id):
        profile = get_object_or_404(Profile, user__id=user_id)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostAPIView(APIView):    
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

class NotificationAPIView(APIView):
    def get(self, request, user):
        notification = get_object_or_404(Notification, user=user)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)
