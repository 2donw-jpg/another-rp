from rest_framework import serializers
from zybal.models import Profile, Post, Notification, FollowersCount



class ProfileMainSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    def get_posts(self, obj):
        posts = Post.objects.filter(user=obj)
        serializer = PostSerializer(posts, many=True)
        return serializer.data

    posts = serializers.SerializerMethodField()

    def get_followers_count(self, obj):
        followers_count = FollowersCount.objects.filter(followed_user=obj).count()
        return followers_count

    followers_count = serializers.SerializerMethodField()

    def get_following_count(self, obj):
        following_count = FollowersCount.objects.filter(follower=obj).count()
        return following_count

    following_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'phone_number', 'bio', 'profile_image', 'email', 'date_joined', 'posts', 'followers_count', 'following_count']

class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ['id','image','caption','created_at', 'likes_count' ]







class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name','profile_image',]


    



class PostMainSerializer(serializers.ModelSerializer):

    user = ProfileSerializer()

    class Meta:
        model = Post
        fields = ['user',"image","caption","created_at", 'user']






        

class NotificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notification
        fields = ['user','sender','notification_type','target_post','is_read','created_at']

class PostUploadSerializer(serializers.Serializer):
    image_upload = serializers.ImageField()
    caption = serializers.CharField(required=False)
    