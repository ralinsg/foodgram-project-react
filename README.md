
# Сайт Foodgram

Продуктовый помощник, в котором пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.


## Для проверки:
e-mail admin@admin.ru

пароль admin

http://51.250.91.194/

## Технологический стек:

- Python 3
- Django
- Django REST ramework
- PostgreSQL
- Djoser
- Gunicorn
- Nginx
- Docker
- Docker Hub
- Yandex.Cloud


## Установка и запуск проекта локально на Windows:

Клонировать репозиторий:
```bash
 git clone https://github.com/ralinsg/foodgram-project-react

```
Перейти в склонированный репозиторий:
```bash
 cd foodgram-project-react
```
Cоздать виртуальное окружение:
```bash
 py 3.7 -m venv venv
```
Активировать виртуальное окружение:
```bash
 source env/bin/activate
```
Установить зависимости из файла requirements.txt:
```bash
 pip install -r requirements.txt
```
Создать файл .env в директории infra со следующими данными:
```bash
SECRET_KEY=<SECRET_KEY из settings.py>
DB_ENGINE='django.db.backends.postgresql'
POSTGRES_DB=<Имя БД>
POSTGRES_USER=<Пользователь БД>
POSTGRES_PASSWORD=<Пароль БД>
DB_HOST='db'
DB_PORT='5432'
ALLOWED_HOSTS=<127.0.0.1, localhost, backend>
DEBUG = False
```
Устанавливаем и запускаем актуальную версию приложения Docker.
[Нажми для перехода на сайт.](https://www.docker.com/products/docker-desktop/)

В директории backend создаем docker образ:
```bash
docker build -t USERNAME/foodgram_backend:v0.1 .
```
В директории frontend создаем docker образ:
```bash
docker build -t USERNAME/foodgram_frontend:v0.1 .
```
В директории infra запускаем docker-compose файл:
```bash
docker-compose up -d --build
```
Создаем миграции:
```bash
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate --noinput
```
Создаем суперпользователя:
```bash
docker-compose exec backend python manage.py createsuperuser
```
Собираем статику:
```bash
docker-compose exec backend python manage.py collectstatic --no-input
```
Загружаем в БД ингредиенты и теги:
```bash
docker-compose exec backend python manage.py download_tags
docker-compose exec backend python manage.py download_ingrs
```
Сайт доступен по адресу:

http://127.0.0.1/

Документация к API доступна после запуска

http://127.0.0.1/api/docs/

Остановить Docker-compose:
```bash
docker-compose stop
```
Удалить ВСЕ данные:
```bash
docker-compose down -v
```
#
## Установка и запуск проекта ВМ Yandex Cloud:

Запустить терминал и выполнить команду:

```bash
ssh login@ip_вашего_сервера
```

Выполнить команду на сервере для установки утилиты по скачиванию файлов:
```bash
sudo apt install curl
```
Выполнить команду по скаивания скрипта для установки Docker:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
```
Запустить скрипт:
```bash
sh get-docker.sh
```
Установить Docker Compose:
```bash
sudo apt install docker-ce docker-compose -y
```
Проверить работу Docker:
```bash
sudo systemctl status docker
```
Создаем директорию infra:
```bash
mkdir infra
```
Локально подключаемся к аккаунту на Docker Hub:
```bash
docker login -u USERNAME
```
Создаем локально docker образы, в директории backend выполнить команду:
```bash
docker build -t USERNAME/foodgram_backend:v0.1 .
```
Загрузить образ backend на Docker Hub:
```bash
docker push USERNAME/foodgram_backend:v0.1
```
Создаем локально docker образы, в директории frontend выполнить команду:
```bash
docker build -t USERNAME/foodgram_frontend:v0.1 .
```
Загрузить образ frontend на Docker Hub:
```bash
docker push USERNAME/foodgram_frontend:v0.1
```
Локально перенести файлы docker-compose.yml и default.conf на сервер:
 ```bash
scp docker-compose.yml USERNAME@ip_вашего_сервера:/home/username/
scp default.conf USERNAME@ip_вашего_сервера:/home/username/
```
Создать файл .env в директории infra со следующими данными:
```bash
SECRET_KEY=<SECRET_KEY из settings.py>
DB_ENGINE='django.db.backends.postgresql'
POSTGRES_DB=<Имя БД>
POSTGRES_USER=<Пользователь БД>
POSTGRES_PASSWORD=<Пароль БД>
DB_HOST='db'
DB_PORT='5432'
ALLOWED_HOSTS=<ip_вашего_сервера, 127.0.0.1, localhost, backend>
DEBUG = False
```


В директории infra запускаем docker-compose файл:
```bash
sudo docker-compose up -d --build
```
Создаем миграции:
```bash
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate --noinput
```
Создаем суперпользователя:
```bash
sudo docker-compose exec backend python manage.py createsuperuser
```
Собираем статику:
```bash
sudo docker-compose exec backend python manage.py collectstatic --no-input
```
Загружаем в БД ингредиенты и теги:
```bash
sudo docker-compose exec backend python manage.py download_tags
sudo docker-compose exec backend python manage.py download_ingrs
```
Сайт доступен по адресу:

http://ip_вашего_сервера/

Остановить Docker-compose:
```bash
sudo docker-compose stop
```
Удалить ВСЕ данные:
```bash
sudo docker-compose down -v
```


## Автор

- [@ralinsg](https://github.com/ralinsg)
