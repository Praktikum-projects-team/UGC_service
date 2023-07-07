# UGC_service
Отправка событий в Kafka и перенос их в ClickHouse для аналитики

# Запуск
Перед запуском создать .env файл по .env.example  
Запуск кликхауса: `cd clickhouse & docker-compose up -d`  
Запуск проекта: `docker-compose up --build`  
Kafka доступна по адресу: http://localhost:9021 

## Исследование хранилищ
[Тут](storage_research/RESEARCH.md)

## Команда разработки
* Лиана Нигматуллина - тимлид
* Татьяна Акимова - разработчик
* Софья Рытик - разработчик
* Анатолий Хабаров - разработчик
