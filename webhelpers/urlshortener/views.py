# django
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse
# rest_framework
from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response

# project
from urlshortener.helpers import alias_generator
from urlshortener.models import LinkPair, Referer
from urlshortener.serializers import LinkPairSerializer, RefererSerializer


class LinkPairView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin):
    queryset = LinkPair.objects
    serializer_class = LinkPairSerializer

    def get(self, request, *args, **kwargs):
        """
            The function returns the result of calling the "list" method with the given request, arguments,
            and keyword arguments.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
            This function handles the POST request for creating a new LinkPair object, setting the
            'is_custom' field based on the presence of an 'alias' field in the request data, generating an
            alias if necessary, and returning the serialized data or any errors.

            :param request: The HTTP request object
            :return: The code is returning a response object. If the serializer is valid, it returns the
            serialized data with a status code of 201 (HTTP_CREATED). If the serializer is not valid, it
            returns the serializer errors with a status code of 400 (HTTP_BAD_REQUEST).
        """
        _mutable: bool = request.data._mutable
        setattr(request.data, '_mutable', True)

        if request.data.get('alias'):
            request.data['is_custom'] = True
        else:
            request.data['is_custom'] = False
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
    """
        The function redirects the user to a target URL based on an alias,
        while also checking if the link is active and secured.

        :param request: The HTTP request object
        :param alias: The `alias` parameter is a unique identifier for a specific link. It is used to
        retrieve the corresponding `LinkPair` object from the database
        :return: a redirect response to the target URL if the alias is found and active. If the alias is not
        found, it returns a response with an error message and a status code of 404. If the alias is found
        but not active, it returns a response with a message indicating that the link is expired and a
        status code of 204.
    """
    try:
        link_pair = LinkPair.objects.get(alias=alias)

        if not link_pair.is_active:
            return Response({'message': 'This link is expired.'}, status.HTTP_204_NO_CONTENT)

        if link_pair.is_secured:
            redirect_url = reverse('password-form', args=[alias])
            return redirect(redirect_url)

        referer_url = request.headers.get('Origin')
        if referer_url:
            data = {
                'referer_url': referer_url,
                'link_pair': link_pair.id
            }
            serializer = RefererSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        link_pair.request_count += 1
        link_pair.save()
        target_url = link_pair.url

        return redirect(target_url)

    except ObjectDoesNotExist:
        return Response({'error': 'Alias not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', 'GET'])
def enter_password(request, alias):
    """
        The function checks if a given password matches the password associated with a specific alias,
        and redirects to a URL if the password is correct.

        :param request: The HTTP request object
        :param alias: The "alias" parameter is a unique identifier for a LinkPair object. It is used to
        retrieve the corresponding LinkPair from the database
        :return: a Response object with a message or error, along with an appropriate HTTP status code.
    """
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


@api_view(['GET'])
def get_request_count(request, alias):
    """
        The function retrieves the request count for a given link alias.

        :param request: The HTTP request object
        :param alias: The "alias" parameter is a unique identifier for a link. It is used to retrieve a
        specific LinkPair object from the database
        :return: a Response object with the request count of a link pair, along with an HTTP status code.
    """
    try:
        link_pair = LinkPair.objects.get(alias=alias)
    except ObjectDoesNotExist:
        return Response({'message': 'This link does not exist.'}, status.HTTP_204_NO_CONTENT)

    request_count = link_pair.request_count
    return Response({'request_count': request_count}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_referers_count(request, alias):
    """
        The function retrieves the top 5 referers for a given link alias and returns
        them in descending order of referer count and trigger date.

        :param request: The HTTP request object
        :param alias: The `alias` parameter is a string that represents the alias of a link
        :return: a Response object with the top 5 referers for a given alias. The referers are sorted by the
        number of times they have been recorded and the date they were triggered. The referers are returned
        in the 'referer_top' field of the response.
    """
    try:
        link_pair_id = LinkPair.objects.get(alias=alias).id
    except ObjectDoesNotExist:
        return Response({'message': 'This link does not exist.'}, status.HTTP_204_NO_CONTENT)

    sorted_referers = \
        Referer.objects.filter(link_pair_id=link_pair_id) \
            .values('referer_url') \
            .annotate(referer_count=Count('referer_url')) \
            .order_by('-referer_count', '-trigger_dt')

    referers_top = sorted_referers[:5]

    return Response({'referer_top': referers_top}, status=status.HTTP_200_OK)
