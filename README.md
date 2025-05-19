# Порядок запуска

## 1. Запуск Redis в Docker (терминал Docker):

`docker run --yt_check redis -p 6379:6379 -d redis`

## 2. Запуск Celery (первый терминал IDE):

`celery -A yt_check worker --loglevel=info --pool=solo`

## 3. Запуск Celery Beat (второй терминал IDE):

`celery -A yt_check beat --loglevel=info`

## 4. Запуск сервера (третий терминал IDE):

`python manage.py runserver`
