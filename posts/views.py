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




