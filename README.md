# blogTestProject
Проект "blogTestProject" с возможностью создания постов в своем блоге и просмотре постов в блогах других пользователей

# КОМАНДЫ ДЛЯ ЗАПУСКА ПРОЕКТА:

(создание виртуального окружения)
### virtualenv myVenv

(использование виртуального окружения)
### source myVenv/bin/activate

(установка зависимостей)
### pip3 install -r requirements.txt

(миграции для работы базы данных)
### python3 manage.py makemigrations
### python3 manage.py migrate

(запуск приложения на локальном сервере)
### python3 manage.py runserver

# ДЛЯ СОЗДАНИЯ СУПЕРЮЗЕРА ДЛЯ ДОСТУПА К АДМИНКИ DJANGO

(создание супер юзера)
### python3 manage.py createsuperuser
(дальше нужно вести логин, (почту можно пропустить) и пароль дважды)

Админка доступна по url:
http://127.0.0.1:8000/admin/
