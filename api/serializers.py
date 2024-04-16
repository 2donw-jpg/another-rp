from rest_framework import serializers
from zybal.models import Profile, Post, Notification



class ProfileSerializer(serializers.ModelSerializer):
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
    

    class Meta:
        model = Profile
        fields = ['id_user','username', 'first_name','last_name','phone_number','bio','profile_image','email', 'date_joined','posts' ]

class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ['id','image','caption','created_at','no_of_likes' ]

class NotificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notification
        fields = ['user','sender','notification_type','target_post','is_read','created_at']