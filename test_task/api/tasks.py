import logging
from django.db import IntegrityError, OperationalError
from django.db.models import F
from celery import shared_task

from .models import Audio, Text, Video


logger = logging.getLogger(__name__)


@shared_task
def increment_counters(content_updates):
    """
    Увеличение счетчиков для списка обновлений содержимого.
    """
    model_map = {
        'Video': Video,
        'Audio': Audio,
        'Text': Text,
    }

    for content_id, content_type in content_updates:
        model = model_map.get(content_type)
        if model:
            try:
                updated_count = model.objects.filter(id=content_id).update(
                    counter=F('counter') + 1
                )
                if updated_count:
                    logger.info(
                        f"Счетчик для {content_type} "
                        f"с id {content_id} увеличен."
                    )
                else:
                    logger.warning(
                        f"{content_type} с id {content_id} не существует."
                    )
            except (IntegrityError, OperationalError) as e:
                logger.error(
                    f"Произошла ошибка БД при увеличении счетчика для "
                    f"{content_type} с id {content_id}: {e}"
                )
        else:
            logger.error(f"Недопустимый тип содержимого: {content_type}.")
