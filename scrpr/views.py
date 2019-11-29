# from secrets import token_hex
# from os import path
from urllib.parse import urlencode
from django.http import Http404
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
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


class FormListView(FormView, MultipleObjectMixin):

    def get(self, request, *args, **kwargs):
        self.form = self.get_form(self.get_form_class())
        self.form.initial = self.get_form_values(request.GET.dict())
        self.object_list = self.get_queryset(self.form.initial)
        self.params = self.get_query_string(request.GET.dict())
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = {
            'form': self.form,
            'params': self.params,
        }
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
    success_url = '/scrpr/favorites/'

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
    success_url = '/scrpr/favorites/'

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
    success_url = '/scrpr/favorites'

    def get_context_data(self, **kwargs):
        context = {
            'title': _('Favorites (Delete)')
        }
        context.update(**kwargs)
        return super().get_context_data(**context)


class FavoritesJobDeleteView(FavoritesMixin, DeleteView):
    template_name = 'scrpr/content_with_sidebar/delete_favorites_job.html'
    model = FavoriteJobQuery
    success_url = '/scrpr/favorites'

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
    model = Game
    paginate_by = 30
    form_class = GamesForm
    url = 'scrpr:games'
    ordering = 'pk'

    def get_queryset(self, query_items=None):
        if not query_items:
            return super().get_queryset()
        queryset = self.model.objects
        for key, value in query_items.items():
            if key == 'title':
                queryset = queryset.filter(title__icontains=value)
            elif key == 'price_min':
                queryset = queryset.filter(
                    Q(price__gte=value) | Q(psplus_price__gte=value))
            elif key == 'price_max':
                queryset = queryset.filter(
                    Q(price__lte=value) | Q(psplus_price__lte=value))
            elif key == 'psplus_price':
                queryset = queryset.filter(psplus_price__isnull=False)
            elif key == 'initial_price':
                queryset = queryset.filter(initial_price__isnull=False)
            elif key == 'free':
                queryset = queryset.filter(Q(price=0.00) | Q(psplus_price=0.00))
        return queryset

    def get_context_data(self, **kwargs):
        context = {
            'title': _('Games'),
        }
        context.update(kwargs)
        return super().get_context_data(**context)


class JobsView(FormListView):
    template_name = 'scrpr/content_with_sidebar/jobs.html'
    model = Job
    paginate_by = 20
    form_class = JobsForm
    url = 'scrpr:jobs'
    ordering = 'title'

    def get_queryset(self, query_items=None):
        if not query_items:
            return super().get_queryset()
        queryset = self.model.objects
        for key, value in query_items.items():
            if key == 'title':
                queryset = queryset.filter(title__icontains=value)
            elif key == 'city':
                queryset = queryset.filter(location=value)
            elif key == 'salary_min':
                queryset = queryset.filter(salary_min__gte=value)
            elif key == 'salary_max':
                queryset = queryset.filter(salary_max__lte=value)
            elif key == 'with_salary':
                queryset = queryset.filter(
                    salary_min__isnull=False, salary_max__isnull=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = {
            'title': _('Jobs'),
        }
        context.update(kwargs)
        return super().get_context_data(**context)


class CustomLogoutView(LogoutView):
    next_page = '/scrpr/'
    template_name = 'scrpr/index.html'


def freelance(request):
    context = None
    return render(request, 'scrpr/index.html', context)
