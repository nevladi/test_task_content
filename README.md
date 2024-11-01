# Test_task

API на основе Django для управления видео, аудио и текстовым контентом.

## Функционал

* Система управления контентом для видео, аудио и текстов
* Использует фреймворк DRF

## Требования

* Python 3.12
* Django 5.1.2
* Другие зависимости перечислены в файле `requirements.txt`

### Установка

#### Шаг 1: Клонировать репозиторий

```sh
    git clone git@github.com:nevladi/test_task_content.git
```
#### Шаг 2: Перейти в директорию проекта
```sh
    cd test_task_content
```
#### Шаг 3: Создать виртуальное окружение
Для создания виртуального окружения используйте следующую команду:
```sh
    python -m venv venv
```
#### Шаг 4: Активировать виртуальное окружение
На Windows:
```sh
    venv\Scripts\activate
```
На macOS и Linux:
```sh
    source venv/bin/activate
```
#### Шаг 5: Установить зависимости
```sh
    pip install -r requirements.txt
```
#### Шаг 6: Выполнить миграции
```sh
    python manage.py migrate
```
#### Шаг 7: Запустить приложение
```sh
    python manage.py runserver
```
#### Шаг 8: Запустить рабочий процесс Celery
В отдельном терминале, активировав виртуальное окружение, выполните следующую команду:
```sh
    celery -A test_task.celery worker --loglevel=info
```
#### Использование
Доступ к приложению по адресу http://localhost:8000/api/pages/

Управление контентом через интерфейс администратора Django после создания суперпользователя.

Для запуска тестов выполните команду:
```sh
    python manage.py test api.tests
```