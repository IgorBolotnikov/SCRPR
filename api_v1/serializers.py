from rest_framework import serializers

from scrpr.models import *


class NewsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsPost
        fields = ('id', 'title', 'body', 'datetime_posted')


class FavoriteGameQuerySerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()

    class Meta:
        model = FavoriteGameQuery
        fields = (
            'id',
            'title',
            'price_min',
            'price_max',
            'psplus_price',
            'initial_price',
            'free',
            'notification_freq',
            'details'
        )

    def get_details(self, obj):
        return obj.details

class FavoriteJobQuerySerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()

    class Meta:
        model = FavoriteJobQuery
        fields = (
            'id',
            'title',
            'city',
            'salary_min',
            'salary_max',
            'with_salary',
            'notification_freq',
            'details'
        )

    def get_details(self, obj):
        return obj.details
