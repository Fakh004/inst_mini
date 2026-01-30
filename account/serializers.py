from rest_framework import serializers
from .models import User
from posts.serializer import PostSerializer
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    bio = serializers.CharField(source='profile.bio', read_only=True)
    avatar = serializers.ImageField(source='profile.avatar',read_only=True)
    posts_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    posts_user = PostSerializer(many=True,read_only=True,source='posts')

    class Meta:
        model = User
        fields = ('id','username','email','password','bio',"avatar",'posts_count','followers_count','following_count','posts_user',)

    def get_posts_count(self, obj):
        return obj.posts.filter(is_deleted=False).count()

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        UserProfile.objects.create(user=user)  

        return user




class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    bio = serializers.CharField(required=False)

    class Meta:
        model = UserProfile
        fields = ('avatar', 'bio')
