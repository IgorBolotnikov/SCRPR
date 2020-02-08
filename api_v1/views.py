from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api_v1.serializers import NewsPostSerializer, FavoriteGameQuerySerializer
from scrpr.models import NewsPost, FavoriteGameQuery
from api_v1.permissions import IsCreator


class NewsListView(ListAPIView):
    queryset = NewsPost.objects.all()
    serializer_class = NewsPostSerializer
    permission_classes = [AllowAny]
    paginate_by = 10


class FavoritesGamesListView(ModelViewSet):
    serializer_class = FavoriteGameQuerySerializer
    permission_classes = [IsAuthenticated, IsCreator]
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        return FavoriteGameQuery.objects.filter(account=self.request.user)
