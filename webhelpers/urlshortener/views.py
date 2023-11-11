#django
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
# rest_framework
from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
# project
from urlshortener.models import LinkPair
from urlshortener.serializers import LinkPairSerializer


class LinkPairView(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = LinkPair
    serializer_class = LinkPairSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@api_view(['GET'])
def link_redirect(request, code):
    try:
        link_pair = LinkPair.objects.get(short_link=code)
    except ObjectDoesNotExist:
        return Response({'message': 'This link does not exist'}, status.HTTP_204_NO_CONTENT)
    redirect_address = link_pair.long_link
    return redirect(redirect_address)
