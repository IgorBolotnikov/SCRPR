from django.core.cache import cache
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from project.cache import generate_cache_key
from scrpr.models import FavoriteGameQuery, FavoriteJobQuery, NewsPost
from scrpr.paginator import VirtualPaginator
from web_scraper.web_scraping.scrape_games import PSStoreScraper
from web_scraper.web_scraping.scrape_jobs import JobsSitesScraper

from .permissions import IsCreator
from .serializers import (
    CommentSerializer,
    FavoriteGameQuerySerializer,
    FavoriteJobQuerySerializer,
    NewsPostSerializer,
)


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


class PaginatorMixin:
    def get_pagination(self, paginator):
        prev_page = (
            paginator.previous_page_number if paginator.has_previous else None
        )
        next_page = paginator.next_page_number if paginator.has_next else None
        return {
            "page": paginator.number,
            "prev_page": prev_page,
            "next_page": next_page,
            "last_page": paginator.num_pages,
        }


class BaseListAPIView(APIView):
    """
    Child classes have to have 'get_scraped_data' method defined,
    which takes two params: query_params, page_num
    This method should return dictionary in the following format:
    {
        'object_list': [<list of results>],
        'last_page': <int: last page number>
    }
    """

    def get_queryset(self):
        # Get query params
        query_params = self.get_query_params()
        pane_num = int(query_params.get("page", "1")) or 1
        # Check if cache has any value for generated key
        cache_key = generate_cache_key(query_params)
        cached_query = cache.get(cache_key)
        if cached_query:
            # Return results from cache
            query_results = cached_query
        else:
            # Return results from scraping the website
            query_results = self.get_scraped_data(query_params, pane_num)
            # Don't cache if no results were returned
            if (
                query_results.get("object_list")
                and len(query_results["object_list"]) > 0
            ):
                cache.set(cache_key, query_results)
        results = query_results.get("object_list")
        last_page = query_results.get("last_page")
        # Create virtual paginator, since no model is used
        paginator = VirtualPaginator(pane_num, last_page)
        return {
            "pagination": self.get_pagination(paginator),
            "results": results,
        }

    def get(self, request, *args, **kwargs):
        results = self.get_queryset()
        return Response(results, status=status.HTTP_200_OK)


class GamesAPIView(BaseListAPIView, PaginatorMixin):
    permission_classes = [AllowAny]

    def get_query_params(self):
        query_params = self.request.query_params.dict()
        query_params["type"] = "games"
        return query_params

    def get_scraped_data(self, query_params, page_num):
        return PSStoreScraper().scrape_game_website(
            query_params=query_params, page_num=page_num
        )


class JobsAPIView(BaseListAPIView, PaginatorMixin):
    permission_classes = [AllowAny]

    def get_query_params(self):
        query_params = self.request.query_params.dict()
        query_params["type"] = "jobs"
        return query_params

    def get_scraped_data(self, query_params, page_num):
        return JobsSitesScraper().scrape_websites(
            query_params=query_params,
            page_num=page_num,
            location=query_params.get("location"),
        )
