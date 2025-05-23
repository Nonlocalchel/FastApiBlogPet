<h2 align="center">TaskService by Django</h2>

Стартовый шаблон для удобной разработки приложений с FastAPI.
Приложение построено на архитектуре mvp. Взаимодействие с базой на шаблоне repository.
Структура не разделена на работу с бизнес-сущностями для удобной работы с маршрутами, версией API и зависимостями ручек.
Для создания новой таблицы следует прописать класс в backend/core/models и указать его имя для
импорта в __init__ файле пакета. Для работы с бизнес-сущностями надо создать соответсвующий 
сервис(пример : /backend/services/posts_services.py) и создать обьект в  api/dependencies/services.py. 
Далее можно использовать service в ручках
Стандартный сервис поддерживает операции все CRUD операции<br>
Тест: https://github.com/Nonlocalchel/drf_test/blob/main/manual.md
### Инструменты разработки

**Стек:**
- Python >= 3.8
- FastAPI
- Postgres

## Старт

#### 1) Создать образ

    docker-compose build

##### 2) Запустить контейнер

    docker-compose up
    
##### 3) Перейти по адресу

    http://127.0.0.1:8001/docs/
## Разработка с Docker

##### 1) Сделать форк репозитория

##### 2) Клонировать репозиторий

    git clone ссылка_сгенерированная_в_вашем_репозитории

##### 3) В корне проекта создать .env и .env.appconfig в /backend. Формат окуржения описан в .<env_name>.template файлах

    
##### 4) Создать образ

    docker-compose build

##### 5) Запустить контейнер

    docker-compose up
    
##### 6) Создать суперюзера

    docker exec -it backend python $APP_HOME/actions/create_super_user.py

## Unit - тесты
Тесты используют отдельный контейнер с БД. В начале тестирования автоматически применяються миграции.</br>
В конце данные удаляються из БД с помощью команды TRUNCATE
- Запустить docker-compose с базой для тестирования:
    ```
    docker-compose docker-compose-local.yaml build
    docker-compose docker-compose-local.yaml up
    ```
- Перейти в директорию с тестами backend-приложения:
    ```
    cd backend
    ```
- Запустить все тесты:
  ```
    pytest -s
  ```
