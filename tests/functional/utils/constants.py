import os

from dotenv import load_dotenv

# Загрузка переменных из файла .env для локального запуска тестов
load_dotenv()


class UserData:
    LOGIN = "user@test.ru"
    PASSWORD = "123qwe"
    NAME = "test_user"
