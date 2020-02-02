# lists/tests.py

from django.test import TestCase


class HomePageTest(TestCase):

    def test_users_home_template(self):
        response = self.client.get('/')  # URLの解決
        self.assertTemplateUsed(response, 'lists/home.html')
