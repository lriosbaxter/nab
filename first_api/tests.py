from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class HelloWorldTestCase(APITestCase):

    def test_hello_world(self):
        response = self.client.get(reverse('hello-world'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'], 'Hello, world!')
