import asyncio
from urllib.parse import urlencode, parse_qs
from django.http import Http404
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.core.cache import cache
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView, MultipleObjectMixin
from django.views.generic.edit import (
    View,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
    DeletionMixin
)
from authentication.models import User
from .forms import *
from .models import *
from .constants import *
from.paginator import VirtualPaginator
from web_scraper.web_scraping.scrape_games import PSStoreScraper
from web_scraper.web_scraping.scrape_jobs import JobsSitesScraper


def generate_cache_key(query):
    key = ','.join([f'{key}-{str(value).lower()}' for key, value in query.items()])
    return hash(key)


class FormListView(FormView):
    def get(self, request, *args, **kwargs):
        self.form = self.get_form(self.get_form_class())
        self.form.initial = self.get_form_values(request.GET.dict())
        self.current_page = self.get_current_page(request.META['QUERY_STRING'])
        self.params = self.get_query_string(self.form.initial)
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_current_page(self, query_string):
        page_field = parse_qs(query_string).get('page')
        page_num = page_field[0] if page_field else '1'
        return int(page_num) if page_num.isnumeric() else 1

    def get_context_data(self, **kwargs):
        context = {
            'form': self.form,
            'params': self.params,
            'object_list': self.get_queryset(self.form.initial)
        }
        if self.last_page > 1:
            context['page_obj'] = VirtualPaginator(
                self.current_page,
                self.last_page
            )
        context.update(kwargs)
        return super().get_context_data(**context)

    def get_form_values(self, dictionary):
        result = {}
        for key, value in dictionary.items():
            if key not in NON_FORM_VALUES and value:
                result[key] = value
        return result

    def get_query_string(self, params):
        return urlencode(params)

    def redirect_with_params(self, url, params=None):
        response = redirect(url)
        if params:
            query_string = self.get_query_string(params)
            response['Location'] += '?' + query_string
        return response

    def post(self, request, *args, **kwargs):
        params = self.get_form_values(request.POST.dict())
        if request.POST.get('save_to_favorites'):
            kwargs = {'account': request.user.id}
            kwargs.update(params)
            form_kwargs = {
                'initial': self.get_initial(),
                'prefix': self.get_prefix(),
                'data': kwargs,
                'files': None
            }
            form = self.form_class(**form_kwargs)
            if form.is_valid():
                form.save()
        return self.redirect_with_params(self.url, params)


class MainPageView(TemplateView):
    template_name = 'scrpr/index.html'

    def get_context_data(self, **kwargs):
        context = {
            'title': _('Home')
        }
        context.update(**kwargs)
        return super().get_context_data(**context)


class NewsListView(ListView):
    template_name = 'scrpr/news.html'
    model = NewsPost

    def get_context_data(self, **kwargs):
        context = {
            'title': _('News')
        }
        context.update(**kwargs)
        return super().get_context_data(**context)


class FavoritesView(LoginRequiredMixin, TemplateView):
    login_url = '/auth/login/'
    template_name = 'scrpr/content_with_sidebar/favorites.html'
    model_games = FavoriteGameQuery
    model_jobs = FavoriteJobQuery

    def get(self, request, *args, **kwargs):
        self.user_id = request.user.id
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Favorites')
        context['object_list_games'] = self.model_games.objects.filter(
            account=self.user_id)
        context['object_list_jobs'] = self.model_jobs.objects.filter(
            account=self.user_id)
        return context


class FavoritesMixin(LoginRequiredMixin):
    login_url = '/auth/login/'

    def get(self, request, *args, **kwargs):
        if self.get_object().account.id != request.user.id:
            raise Http404()
        else:
            return super().get(request, *args, **kwargs)


class FavoritesGameDetailView(FavoritesMixin, UpdateView):
    template_name = 'scrpr/content_with_sidebar/favorites_game.html'
    model = FavoriteGameQuery
    form_class = GamesForm
    template_name_suffix = ''
    success_url = '/favorites/'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        params = {'account': request.user.id}
        params.update(request.POST.dict())
        form_kwargs = {
            'prefix': self.get_prefix(),
            'data': params,
            'instance': self.object
        }
        form = self.form_class(**form_kwargs)
        if form.is_valid():
            self.form_valid(form)
            # self.object = form.save()
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = {
            'title': _('Favorites (Edit)')
        }
        context.update(**kwargs)
        return super().get_context_data(**context)


class FavoritesJobDetailView(FavoritesMixin, UpdateView):
    template_name = 'scrpr/content_with_sidebar/favorites_job.html'
    model = FavoriteJobQuery
    form_class = JobsForm
    template_name_suffix = ''
    success_url = '/favorites/'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        params = {'account': request.user.id}
        params.update(request.POST.dict())
        form_kwargs = {
            'prefix': self.get_prefix(),
            'data': params,
            'instance': self.object
        }
        form = self.form_class(**form_kwargs)
        if form.is_valid():
            self.form_valid(form)
            # self.object = form.save()
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = {
            'title': _('Favorites (Edit)')
        }
        context.update(**kwargs)
        return super().get_context_data(**context)


class FavoritesGameDeleteView(FavoritesMixin, DeleteView):
    template_name = 'scrpr/content_with_sidebar/delete_favorites_game.html'
    model = FavoriteGameQuery
    success_url = '/favorites'

    def get_context_data(self, **kwargs):
        context = {
            'title': _('Favorites (Delete)')
        }
        context.update(**kwargs)
        return super().get_context_data(**context)


class FavoritesJobDeleteView(FavoritesMixin, DeleteView):
    template_name = 'scrpr/content_with_sidebar/delete_favorites_job.html'
    model = FavoriteJobQuery
    success_url = '/favorites'

    def get_context_data(self, **kwargs):
        context = {
            'title': _('Favorites (Delete)')
        }
        context.update(**kwargs)
        return super().get_context_data(**context)


class AboutView(TemplateView):
    template_name = 'scrpr/about.html'

    def get_context_data(self, **kwargs):
        context = {
            'title': _('About')
        }
        context.update(**kwargs)
        return super().get_context_data(**context)


class RateView(CreateView):
    template_name = 'scrpr/rate.html'
    form_class = RateForm
    success_url = '/scrpr'

    def get_context_data(self, **kwargs):
        context = {
            'title': _('Rate!')
        }
        context.update(**kwargs)
        return super().get_context_data(**context)


class GamesView(FormListView):
    template_name = 'scrpr/content_with_sidebar/games.html'
    form_class = GamesForm
    url = 'scrpr:games'

    def get_cache_key(self, query_params):
        page_num = self.current_page if self.current_page else 1
        query_params = query_params if query_params else {'games': 'all'}
        query_params.update({'page': page_num})
        return generate_cache_key(query_params)

    def get_queryset(self, query_params=None):
        cache_key = self.get_cache_key(query_params)
        cached_query = cache.get(cache_key)
        if cached_query:
            query_results = cached_query
        else:
            query_results = PSStoreScraper().scrape_game_website(
                query_params=query_params,
                page_num=self.current_page,
            )
            cache.set(cache_key, query_results, 600)
        self.last_page = query_results.get('last_page', 1)
        return query_results.get('object_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] =  _('Games')
        return context


class JobsView(FormListView):
    template_name = 'scrpr/content_with_sidebar/jobs.html'
    form_class = JobsForm
    url = 'scrpr:jobs'

    def get_cache_key(self, query_params):
        page_num = self.current_page if self.current_page else 1
        query_params = query_params if query_params else {'jobs': 'all'}
        query_params.update({'page': page_num})
        return generate_cache_key(query_params)

    def get_queryset(self, query_params=None):
        cache_key = self.get_cache_key(query_params)
        cached_query = cache.get(cache_key)
        if cached_query:
            query_results = cached_query
        else:
            query_results = JobsSitesScraper().scrape_websites(
                location=query_params.get('city') if query_params else None,
                query_params=query_params,
                page_num=self.current_page,
            )
            cache.set(cache_key, query_results, 600)
        self.last_page = query_results.get('last_page', 1)
        return query_results.get('object_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Jobs')
        return context


class CustomLogoutView(LogoutView):
    next_page = '/scrpr/'
    template_name = 'scrpr/index.html'


def freelance(request):
    context = None
    return render(request, 'scrpr/index.html', context)
