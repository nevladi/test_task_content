import logging
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Page
from .serializers import PageSerializer
from .tasks import increment_counters


logger = logging.getLogger(__name__)


class PagePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class PageListView(generics.ListAPIView):
    """
    Конечная точка API, позволяющая просматривать страницы.
    Возвращает список страниц с их названиями и подробными URL-адресами.
    """
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    pagination_class = PagePagination
    ordering = ['id']

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        new_results = []
        for page in response.data['results']:
            new_result = {
                'id': page['id'],
                'title': page['title'],
                'detail_url': request.build_absolute_uri(
                    f'/api/pages/{page["id"]}/'
                )
            }
            new_results.append(new_result)

        response.data['results'] = new_results
        return Response(response.data)


class PageDetailView(APIView):
    """
    Возвращает подробное представление страницы.
    - Предварительно находит связанное видео, аудио и текстовое содержимое.
    - Увеличивает счетчики для всех типов контента в фоновом режиме.
    """
    def get(self, request, pk):
        try:
            page = Page.objects.prefetch_related(
                'video_content', 'audio_content', 'text_content'
            ).get(id=pk)

            content_updates = []
            for video in page.video_content.all():
                content_updates.append((video.id, 'Video'))

            for audio in page.audio_content.all():
                content_updates.append((audio.id, 'Audio'))

            for text in page.text_content.all():
                content_updates.append((text.id, 'Text'))

            logger.info(f"Обновление счетчиков для: {content_updates}")

            increment_counters.delay(content_updates)

            serializer = PageSerializer(page)
            return Response(serializer.data)
        except Page.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
