from rest_framework import serializers
from .models import Post, Follow, Like, Comment
from account.models import User




class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at']



class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True) 
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
   

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'image', 'created_at', 'updated_at', 'likes_count', 'comments_count',"comments"]





class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField(read_only=True)
    following = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']

    def validate(self, attrs):
        user = self.context['request'].user
        following = attrs['following']

        if user == following:
            raise serializers.ValidationError(
                {"following": "Нельзя подписаться на самого себя"}
            )

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        following = validated_data['following']

        follow, created = Follow.objects.get_or_create(
            follower=user,
            following=following
        )

        if not created:
            follow.delete()
            return None

        return follow



class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user']


