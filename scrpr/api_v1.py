from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from django.core.cache import cache

from project.cache import generate_cache_key
from web_scraper.web_scraping.scrape_games import PSStoreScraper
from web_scraper.web_scraping.scrape_jobs import JobsSitesScraper
from .paginator import VirtualPaginator


class PaginatorMixin:
    def get_pagination(self, paginator):
        prev_page = paginator.previous_page_number if paginator.has_previous else None
        next_page = paginator.next_page_number if paginator.has_next else None
        return {
            'page': paginator.number,
            'prev_page': prev_page,
            'next_page': next_page,
            'last_page': paginator.num_pages
        }


class BaseListAPIView(APIView):
    '''
    Child classes have to have 'get_scraped_data' method defined,
    which takes two params: query_params, page_num
    This method should return dictionary in the following format:
    {
        'object_list': [<list of results>],
        'last_page': <int: last page number>
    }
    '''
    def get_queryset(self):
        # Check that 'get_scraped_data' method exists
        if not hasattr(self, 'get_scraped_data'):
            raise AttributeError(
                "%s class doesn't have 'get_scraped_data' "
                "method defined" % self.__class__.__name__
            )
        # Get query params
        query_params = self.request.query_params.dict()
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
            if query_results.get('object_list') and len(query_results['object_list']) > 0:
                cache.set(cache_key, query_results)
        results = query_results.get('object_list')
        last_page = query_results.get("last_page")
        # Create virtual paginator, since no model is used
        paginator = VirtualPaginator(pane_num, last_page)
        return {
            'pagination': self.get_pagination(paginator),
            'results': results
        }

    def get(self, request, *args, **kwargs):
        results = self.get_queryset()
        return Response(results, status=status.HTTP_200_OK)


class GamesAPIView(BaseListAPIView, PaginatorMixin):
    permission_classes = [AllowAny]

    def get_scraped_data(self, query_params, page_num):
        query_params["type"] = "games"
        return PSStoreScraper().scrape_game_website(
            query_params=query_params,
            page_num=page_num
        )


class JobsAPIView(BaseListAPIView, PaginatorMixin):
    permission_classes = [AllowAny]

    def get_scraped_data(self, query_params, page_num):
        query_params["type"] = "jobs"
        return JobsSitesScraper().scrape_websites(
            query_params=query_params,
            page_num=page_num,
            location=query_params.get("location")
        )
