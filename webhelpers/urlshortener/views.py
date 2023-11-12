# django
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
# rest_framework
from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
# project
from urlshortener.models import LinkPair
from urlshortener.serializers import LinkPairSerializer
from urlshortener.helpers import alias_generator


class LinkPairView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin):
    queryset = LinkPair.objects
    serializer_class = LinkPairSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        _mutable: bool = request.data._mutable
        setattr(request.data, '_mutable', True)

        if request.data.get('alias'):
            request.data['is_custom'] = True
        else:
            alias = alias_generator()
            request.data['alias'] = alias

        setattr(request.data, '_mutable', _mutable)
        serializer = LinkPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def link_redirect(request, alias):
    try:
        link_pair = LinkPair.objects.get(alias=alias)
    except ObjectDoesNotExist:
        return Response({'message': 'This link does not exist.'}, status.HTTP_204_NO_CONTENT)

    if not link_pair.is_active:
        return Response({'message': 'This link is expired.'}, status.HTTP_204_NO_CONTENT)

    link_pair.request_count += 1
    link_pair.save()
    target_url = link_pair.url
    return redirect(target_url)


@api_view(['GET'])
def request_count(request, alias):
    try:
        link_pair = LinkPair.objects.get(alias=alias)
    except ObjectDoesNotExist:
        return Response({'message': 'This link does not exist.'}, status.HTTP_204_NO_CONTENT)

    request_count = link_pair.request_count
    return Response({'request_count': request_count}, status.HTTP_200_OK)
