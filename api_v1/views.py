from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from scrpr.models import *
from api_v1.serializers import *
from api_v1.permissions import IsCreator


class CommentView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]


class NewsListView(ListAPIView):
    queryset = NewsPost.objects.all()
    serializer_class = NewsPostSerializer
    permission_classes = [AllowAny]
    paginate_by = 10


class FavoritesGamesListView(ModelViewSet):
    serializer_class = FavoriteGameQuerySerializer
    permission_classes = [IsAuthenticated, IsCreator]
    paginate_by = 10

    def perform_create(self, serializer):
        serializer.save(account=self.request.user)

    def get_queryset(self, *args, **kwargs):
        return FavoriteGameQuery.objects.filter(account=self.request.user)


class FavoritesJobsListView(ModelViewSet):
    serializer_class = FavoriteJobQuerySerializer
    permission_classes = [IsAuthenticated, IsCreator]
    paginate_by = 10

    def perform_create(self, serializer):
        serializer.save(account=self.request.user)

    def get_queryset(self, *args, **kwargs):
        return FavoriteJobQuery.objects.filter(account=self.request.user)
