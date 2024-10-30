from django.db import models


class Page(models.Model):
    title = models.CharField(max_length=255)

    def get_content(self):
        return (
            list(self.video_content.all()) +
            list(self.audio_content.all()) +
            list(self.text_content.all())
        )

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"

    def __str__(self):
        return self.title


class Content(models.Model):
    title = models.CharField(max_length=255)
    counter = models.PositiveIntegerField(default=0)
    page = models.ForeignKey(
        Page, related_name='%(class)s_content', on_delete=models.CASCADE
    )

    class Meta:
        abstract = True


class Video(Content):
    video_url = models.URLField()
    subtitles_url = models.URLField()

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"

    def __str__(self):
        return self.title


class Audio(Content):
    bitrate = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Аудио"
        verbose_name_plural = "Аудио"

    def __str__(self):
        return self.title


class Text(Content):
    text = models.TextField()

    class Meta:
        verbose_name = "Текст"
        verbose_name_plural = "Тексты"

    def __str__(self):
        return self.title
