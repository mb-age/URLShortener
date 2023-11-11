from rest_framework import serializers
from urlshortener.models import LinkPair
from urlshortener.helpers import link_generator


class LinkPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkPair
        fields = '__all__'

    def create(self, validated_data):
        short_link = self.create_short_link()
        validated_data['short_link'] = short_link
        return super().create(validated_data)

    def create_short_link(self):
        short_link = link_generator()
        while LinkPair.objects.filter(short_link=short_link).exists():
            short_link = link_generator()
        return short_link
