from core.permissions import IsAdminOrReadOnly
from rest_framework import generics
from django.contrib.auth import get_user_model
User = get_user_model()

class PermissionAndPaginationMixin:
    """Возвращает список тегов и ингридиентов."""

    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None

class RetrieveDestroyListCreate(
        generics.RetrieveDestroyAPIView,
        generics.ListCreateAPIView):

    pass

class GetIsSubscribedMixin:

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return user.follower.filter(author=obj).exists()
