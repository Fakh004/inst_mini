# apps/posts/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Post, Follow, Like, Comment
from .serializer import PostSerializer, FollowSerializer, LikeSerializer, CommentSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from account.pagination import CustomPagination
from django.core.cache import cache 



class AllUserPostView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        data = cache.get('My_list')
        if not data:
            serializer=self.get_serializer(self.get_queryset(),many=True)
            data = serializer.data
            cache.set('My_list',data,30)
        return Response (data)
    

   


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.filter(is_deleted=False).select_related('author')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        data = cache.get('My_list')
        if not data:
            serializer=self.get_serializer(self.get_queryset(),many=True)
            data = serializer.data
            cache.set('My_list',data,30)
        return Response (data)
    

    

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.filter(is_deleted=False).select_related('author')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()



class FollowListCreateView(generics.ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

    def post(self, request):
        user = request.user
        following_id = request.data.get('following')

        if not following_id:
            return Response(
                {"following": "Обязательное поле"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if str(user.id) == str(following_id):
            return Response(
                {"following": "Нельзя подписаться на себя"},
                status=status.HTTP_400_BAD_REQUEST
            )

        follow = Follow.objects.filter(
            follower=user,
            following_id=following_id
        )

        if follow.exists():
            follow.delete()
            return Response(
                {"detail": "Отписка выполнена"},
                status=status.HTTP_200_OK
            )

        Follow.objects.create(
            follower=user,
            following_id=following_id
        )

        return Response(
            {"detail": "Подписка выполнена"},
            status=status.HTTP_201_CREATED
        )
    
    def get(self, request, *args, **kwargs):
        data = cache.get('My_list')
        if not data:
            serializer=self.get_serializer(self.get_queryset(),many=True)
            data = serializer.data
            cache.set('My_list',data,30)
        return Response (data)
    


class UnfollowDestroyView(generics.DestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        following_id = self.kwargs['following_id']
        return Follow.objects.get(follower=self.request.user, following_id=following_id)




class LikeCreateDestroyView(generics.GenericAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]


    
    def post(self, request, post_id):  
        user = request.user

        like = Like.objects.filter(
            user=user,
            post_id=post_id
        )

        if like.exists():
            like.delete()
            return Response(
                {"detail": "Лайк убран"},
                status=status.HTTP_200_OK
            )

        Like.objects.create(
            user=user,
            post_id=post_id
        )

        return Response(
            {"detail": "Лайк поставлен"},
            status=status.HTTP_201_CREATED
        )


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.filter(
        is_deleted=False
    ).select_related(
        'author'
    ).prefetch_related(
        'comments__author',
        'likes'
    )
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        data = cache.get('My_list')
        if not data:
            serializer=self.get_serializer(self.get_queryset(),many=True)
            data = serializer.data
            cache.set('My_list',data,30)
        return Response (data)
    


