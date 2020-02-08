from rest_framework import serializers

from scrpr.models import NewsPost


class NewsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsPost
        fields = ('title', 'body', 'datetime_posted')
