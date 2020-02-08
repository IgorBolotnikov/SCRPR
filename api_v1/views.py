from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from api_v1.serializers import NewsPostSerializer
from scrpr.models import NewsPost


class NewsListView(ListAPIView):
    queryset = NewsPost.objects.all()
    serializer_class = NewsPostSerializer
    permission_classes = [AllowAny]
    paginate_by = 10
