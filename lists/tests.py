# lists/tests.py

from django.test import TestCase


class HomePageTest(TestCase):

    def test_users_home_template(self):
        response = self.client.get('/')  # URLの解決
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': "A new list item"})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'lists/home.html')
