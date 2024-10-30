from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Page, Video, Audio, Text


class PageAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.page = Page.objects.create(title="Test Page")
        cls.video = Video.objects.create(
            title="Test Video", page=cls.page,
            video_url="http://example.com/video",
            subtitles_url="http://example.com/subtitles"
        )
        cls.audio = Audio.objects.create(
            title="Test Audio", page=cls.page, bitrate=128
        )
        cls.text = Text.objects.create(
            title="Test Text", page=cls.page, text="Some sample text"
        )

    def test_page_list_api(self):
        """
        Тест API для получения списка страниц с поддержкой пагинации."""
        url = reverse('page-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertTrue(any(
            page['title'] == "Test Page" for page in response.data['results']
        ))

    def test_page_detail_api(self):
        """
        Тест API для получения детальной информации
        о странице и увеличения счетчиков.
        """
        url = reverse('page-detail', args=[self.page.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Page")

        self.assertIn('video_content', response.data)
        self.assertIn('audio_content', response.data)
        self.assertIn('text_content', response.data)

        self.video.refresh_from_db()
        self.audio.refresh_from_db()
        self.text.refresh_from_db()

        self.assertEqual(self.video.counter, 1)
        self.assertEqual(self.audio.counter, 1)
        self.assertEqual(self.text.counter, 1)
