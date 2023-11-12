from rest_framework import serializers, exceptions
from urlshortener.models import LinkPair


class LinkPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkPair
        fields = '__all__'

    def validate_alias(self, data):
        if LinkPair.objects.filter(alias=data).exists():
            raise exceptions.ValidationError({'alias': 'Alias is not available.'})
        if len(data) < 5:
            raise exceptions.ValidationError({'alias': 'The Alias must be at least 5 characters.'})
        return data
