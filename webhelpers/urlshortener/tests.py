from django.test import TestCase
from rest_framework.test import APITestCase

from urlshortener.models import LinkPair


class TestAPI(APITestCase):
    """ Testing POST requests """
    url = '/api/url'

    def test_link_pair_get(self):
        """ Checking for receiving an existing pair """
        existing_data = {
            'url': 'https://www.google.com',
            'alias': 'dJty5167',
        }
        response_get = self.client.post(self.url, data=existing_data)
        result_get = response_get.json()

        self.assertEqual(response_get.status_code, 201)
        self.assertEqual(LinkPair.objects.all().count(), 1)
        self.assertEqual(result_get['url'], 'https://www.google.com')
        self.assertEqual(result_get['alias'], 'dJty5167')
        self.assertIsInstance(result_get, dict)
        self.assertEqual(len(result_get), 8)

    def test_link_pair_create(self):
        """
        Checking the creation of a link pair with and without an explicit alias
        """
        creation_data = {
            'url': 'https://www.python.org/'
        }
        creation_data_with_alias = {
            'url': 'https://www.w3schools.com/',
            'alias': 'A3Ny01io'
        }
        response_create = self.client.post(self.url, data=creation_data)
        result_create = response_create.json()

        response_create_with_alias = self.client.post(self.url, data=creation_data_with_alias)
        result_create_with_alias = response_create_with_alias.json()

        self.assertEqual(response_create.status_code, 201)
        self.assertEqual(result_create['url'], 'https://www.python.org/')
        self.assertEqual(len(result_create['alias']), 8)
        self.assertIsInstance(result_create, dict)
        self.assertEqual(LinkPair.objects.all().count(), 2)
        self.assertEqual(len(result_create), 8)
        self.assertEqual(
            result_create_with_alias['url'],
            'https://www.w3schools.com/',
            msg='URL error'
        )
        self.assertEqual(
            result_create_with_alias['alias'],
            'A3Ny01io',
            msg='Alias error'
        )


class TestRedirection(TestCase):
    """ Testing GET requests """
    active_url = '/api/url/aEdj01'
    deactive_url = '/api/url/q2Nb23'

    def setUp(self) -> None:
        LinkPair.objects.create(
            url='https://www.python.org/',
            alias='aEdj01',
        )

        LinkPair.objects.create(
            url='https://stackoverflow.com/',
            alias='q2Nb23',
            is_active=False
        )

    def test_redirection(self):
        """ Redirect testing """
        response = self.client.get(self.active_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'https://www.python.org/')

    def test_request_counter(self):
        """ Request count testing """
        self.assertEqual(
            LinkPair.objects.get(alias='aEdj01').request_count, 0
        )
        self.client.get(self.active_url)
        self.assertEqual(
            LinkPair.objects.get(alias='aEdj01').request_count, 1
        )
        self.assertEqual(
            LinkPair.objects.get(alias='q2Nb23').request_count, 0
        )
        self.client.get(self.deactive_url)
        self.assertEqual(
            LinkPair.objects.get(alias='q2Nb23').request_count, 0
        )

    def test_deactive_url(self):
        """ Deactive alias testing """
        response = self.client.get(self.deactive_url)
        self.assertEqual(response.content, b'')
