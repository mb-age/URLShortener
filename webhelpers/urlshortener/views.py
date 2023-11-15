# django
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse
# rest_framework
from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response

# project
from urlshortener.helpers import alias_generator
from urlshortener.models import LinkPair
from urlshortener.serializers import LinkPairSerializer


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
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def link_redirect(request, alias):
    try:
        link_pair = LinkPair.objects.get(alias=alias)

        if not link_pair.is_active:
            return Response({'message': 'This link is expired.'}, status.HTTP_204_NO_CONTENT)

        if link_pair.is_secured:
            redirect_url = reverse('password-form', args=[alias])
            return redirect(redirect_url)

        link_pair.request_count += 1
        link_pair.save()
        target_url = link_pair.url
        return redirect(target_url)

    except ObjectDoesNotExist:
        return Response({'error': 'Alias not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_request_count(request, alias):
    try:
        link_pair = LinkPair.objects.get(alias=alias)
    except ObjectDoesNotExist:
        return Response({'message': 'This link does not exist.'}, status.HTTP_204_NO_CONTENT)

    request_count = link_pair.request_count
    return Response({'request_count': request_count}, status.HTTP_200_OK)


@api_view(['POST'])
def put_password(request):
    password = request.data.get('password')
    alias = request.data.get('alias')
    link_pair = LinkPair.objects.get(alias=alias)

    if password != link_pair.password:
        return Response({'message': "The password is wrong"})

    link_pair.request_count += 1
    link_pair.save()
    target_url = link_pair.url
    return redirect(target_url)


@api_view(['POST', 'GET'])
def enter_password(request, alias):
    try:
        link_pair = LinkPair.objects.get(alias=alias)
        if request.method == 'GET':
            return Response({'message': 'Please enter the password'}, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            password = request.data.get('password')
            if password == link_pair.password:
                link_pair.request_count += 1
                link_pair.save()
                return redirect(link_pair.url)
            else:
                return Response({'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except ObjectDoesNotExist:
        return Response({'error': 'Alias not found'}, status=status.HTTP_404_NOT_FOUND)
