from rest_framework import serializers, exceptions
from urlshortener.models import LinkPair


class LinkPairSerializer(serializers.ModelSerializer):
    is_custom = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    request_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = LinkPair
        fields = ['url', 'alias', 'created_dt', 'is_custom', 'is_active', 'request_count']
        extra_kwargs = {'alias': {'validators': []}}

    def validate_alias(self, data):
        if LinkPair.objects.filter(alias=data).exists():
            raise exceptions.ValidationError({'alias': 'Alias is not available.'})
        if len(data) < 5:
            raise exceptions.ValidationError({'alias': 'The Alias must be at least 5 characters.'})
        return data
