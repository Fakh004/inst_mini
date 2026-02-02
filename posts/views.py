from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import *
from .serializer import *
from rest_framework.parsers import MultiPartParser, FormParser
from account.pagination import CustomPagination
from django.core.cache import cache 
from django.shortcuts import get_object_or_404
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema



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


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        p_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user, post_id=p_id)



class SendMessageToUserView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        recipient_id = self.kwargs.get('recipient_id')
        recipient = get_object_or_404(User, id=recipient_id)
        me = self.request.user

        if me == recipient:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Нельзя писать самому себе.")

        chat = Chats.objects.filter(
            (Q(user1=me) & Q(user2=recipient)) | 
            (Q(user1=recipient) & Q(user2=me))
        ).first()

        if not chat:
            chat = Chats.objects.create(
                title=f"Чат {me.username} и {recipient.username}",
                user1=me,
                user2=recipient
            )
        serializer.save(sender=me, chat=chat)

class ChatMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs.get('chat_id')
        return Message.objects.filter(
            Q(chat_id=chat_id) & (Q(chat__user1=self.request.user) | Q(chat__user2=self.request.user))
        )