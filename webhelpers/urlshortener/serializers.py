from rest_framework import serializers, exceptions

from urlshortener.models import LinkPair, Referer


class LinkPairSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    request_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = LinkPair
        fields = ['url', 'alias', 'created_dt', 'is_custom', 'is_active', 'request_count', 'is_secured', 'password']
        extra_kwargs = {'alias': {'validators': []}}

    def validate_alias(self, data):
        """
            Checks if a given alias is available and has a minimum length of 5 characters.

            :param data: The `data` parameter is the alias that needs to be validated
            :return: the `data` parameter if it passes the validation checks.
        """
        if LinkPair.objects.filter(alias=data).exists():
            raise exceptions.ValidationError({'alias': 'Alias is not available.'})
        if len(data) < 5:
            raise exceptions.ValidationError({'alias': 'The Alias must be at least 5 characters.'})
        return data

    def validate(self, attrs):
        """
            Validates attributes and raises an exception if a password is required but not provided.

            :param attrs: The `attrs` parameter is a dictionary that contains the attributes of the
            object being validated. It is used to access and validate specific attributes of the object
            :return: The result of calling the `validate` method of the parent class.
        """
        if attrs.get('is_secured') and not attrs.get('password'):
            raise exceptions.ValidationError({'password': 'Protected alias requires a password.'})
        return super().validate(attrs)


class RefererSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referer
        fields = ['referer_url', 'link_pair', 'trigger_dt']
