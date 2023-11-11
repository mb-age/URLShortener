from rest_framework import serializers
from webhelpers.urlshortener.models import LinkPair


class LinkPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkPair
        fields = '__all__'
