from rest_framework import serializers

from scrpr.models import *


class NewsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsPost
        fields = ('title', 'body', 'datetime_posted')


class FavoriteGameQuerySerializer(serializers.ModelSerializer):
    notification_frequency = serializers.CharField(
        source='get_notification_freq_display'
    )

    class Meta:
        model = FavoriteGameQuery
        fields = (
            'title',
            'price_min',
            'price_max',
            'psplus_price',
            'initial_price',
            'free',
            'notification_frequency'
        )

class FavoriteJobQuerySerializer(serializers.ModelSerializer):
    notification_frequency = serializers.CharField(
        source='get_notification_freq_display'
    )

    class Meta:
        model = FavoriteJobQuery
        fields = (
            'title',
            'city',
            'salary_min',
            'salary_max',
            'with_salary',
            'notification_frequency',
        )
