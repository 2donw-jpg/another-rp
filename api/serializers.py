from rest_framework import serializers
from zybal.models import Profile, Post, Notification, FollowersCount
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','image','caption','created_at', 'likes_count']       
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'profile_image']
class ProfileMainSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'phone_number', 'bio', 'profile_image', 'email', 'date_joined', 'posts', 'followers_count', 'following_count']

    def get_posts(self, obj):
        posts = obj.post_set.all()  # Access posts using related manager
        serializer = PostSerializer(posts, many=True)
        return serializer.data
class PostMainSerializer(serializers.ModelSerializer):

    user = ProfileSerializer()
    class Meta:
        model = Post
        fields = ['user', 'image', 'caption', 'created_at','likes_count']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['user','sender','notification_type','target_post','is_read','created_at']