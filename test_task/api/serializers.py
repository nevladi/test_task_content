from rest_framework import serializers
from .models import Page, Video, Audio, Text


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'video_url', 'subtitles_url', 'counter']


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ['id', 'title', 'bitrate', 'counter']


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['id', 'title', 'text', 'counter']


class PageSerializer(serializers.ModelSerializer):
    video_content = VideoSerializer(many=True, read_only=True)
    audio_content = AudioSerializer(many=True, read_only=True)
    text_content = TextSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = [
            'id', 'title', 'video_content', 'audio_content', 'text_content'
        ]
