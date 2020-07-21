from django.urls import resolve, reverse
from django.test import TestCase
from core.views import MainListView
from core.models import Church


class MainListResolveTest(TestCase):
    def test_root_url(self):
        found = resolve('/')
        self.assertEqual(found.func.__name__, MainListView.as_view().__name__)


class CoreViewTests(TestCase):
    def setUp(self):
        self.object = Church.objects.create(
            name='Saint Sofia',
            slug='saint_sofia',
            social_link='www.ty',
            main_order=0,
        )

    def test_main_object(self):
        self.assertEqual(f'{self.object.name}', 'Saint Sofia')
        self.assertEqual(f'{self.object.slug}', 'saint_sofia')
        self.assertEqual(f'{self.object.social_link}', 'www.ty')

    def test_main_list_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Saint Sofia')
        self.assertTemplateUsed(response, 'core/index.html')

    def test_object_detail_view(self):
        response = self.client.get(self.object.get_absolute_url())
        no_response = self.client.get('/saint_sofia1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Saint Sofia')
        self.assertTemplateUsed(response, 'core/object_detail.html')
