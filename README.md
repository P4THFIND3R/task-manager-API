## TaskManager
TaskManager - менеджер задач, при помощи которого можно создавать, изменять и наблюдать за статусами задач в режиме реального времени. Проект разработан с использованием фреймворка FastAPI, данные хранятся в PostgreSQL и Redis, обновление в режиме реального времени реализовано при помощи WebSocket.
## Развертывание
1. Клонируем репозиторий, переходим в него;
   ```
   git clone https://github.com/P4THFIND3R/task-manager-API TaskManager
   cd TaskManager
	```
2. В папке src/ находится файл .sample.env, который необходимо переименовать в .prov.env и заполнить собственными значениями;
3. Запустить Docker-compose. *в контейнере поднимутся само приложение, postgres и redis*.
   ``` shell
   docker compose up --build
	```
После выполнения всех шагов, приложение становится доступным по адресу 
http://localhost:80 (по умолчанию)
## Функционал
 * В приложении представлена система аутентификации на основе JWT и refresh-token:
	   Выдача токенов производится при авторизации, затем, при истечении срока действия JWT в случае, если срок действия refresh-token не истек, оба JWT и refresh-token автоматически выдаются пользователю и сохраняются в httpOnly куках.
	   Данные о пользовательских сессиях хранятся в redis для обеспечения быстродействия работы, так-же предусмотрены меры по защите от утечек JWT и refresh-token.
* В приложении реализован функционал для создания, изменения, удаления и чтения задач для совместной работы в команде. Так-же разработан фильтр задач:
	* поиск конкретной задачи:
	* поиск всех задач пользователя:
	* фильтрация задач пользователя по статусу выполнения.
* Для получения изменений в статусах задач в режиме реального времени был разработан интерфейс при помощи WebSocket;
* Имплементировано логирование работы приложения при помощи библиотеки loguru; 
* Реализовано интеграционное асинхронное тестирование посредством pytest;
* TODO: имплементировать приоритет задач, доступ к задачам на основе ролей пользователей.
## API
Документация и список конечных точек доступны по адресу http://localhost/docs
![image](https://github.com/P4THFIND3R/task-manager-API/assets/102167990/184506e0-d53e-4ffa-a7d6-2fc3c97ff544)
Так-же доступен endpoint WS для получения информация об изменении задач в режиме реального времени:
* ws://localhost:8001/api/tasks/ws/
## Тестирование
Войти в виртуальное окружение из главного каталога программы:
``` shell
cd venv/Scripts
activate
```
Вернуться в главный каталог:
``` shell
cd ..
cd ..
```
Развернуть контейнеры с тестовыми БД PostgreSQL и Redis:
``` shell
cd tests
docker compose up
cd ..
```
Запустить тестирование pytest (прячем warnings, чтобы скрыть depricated предупреждения):
``` shell
pytest -p no:warnings -s
```
В случае успешного прохождения тестов увидим следующее:
![image](https://github.com/P4THFIND3R/task-manager-API/assets/102167990/99024462-cd5f-4d7c-af86-aec0ddd2748d)

## Структура проекта
```
+---alembic
|   |   env.py
|   |   README
|   |   script.py.mako
|   +---versions
+---src
|   |   .dev.env
|   |   .prod.env
|   |   .sample.env
|   |   .test.env
|   |   config.py
|   |   main.py
|   |   __init__.py
|   +---api
|   |   |   __init__.py
|   |   +---endpoints
|   |   |   |   dependencies.py
|   |   |   |   tasks.py
|   |   |   |   users.py
|   |   |   |   __init__.py
|   |   +---schemas
|   |   |   |   task.py
|   |   |   |   user.py
|   |   |   |   __init__.py
|   +---auth
|   |   |   db.py
|   |   |   dependencies.py
|   |   |   exceptions.py
|   |   |   repository.py
|   |   |   router.py
|   |   |   schemas.py
|   |   |   security.py
|   |   |   __init__.py
|   +---database
|   |   |   db.py
|   |   |   models.py
|   |   |   __init__.py
|   +---log
|   |   |   debug.txt
|   |   |   logger.py
|   |   |   __init__.py
|   |   |
|   +---repositories
|   |   |   base_repository.py
|   |   |   task_repository.py
|   |   |   user_repository.py
|   |   |   __init__.py
|   |   |
|   +---services
|   |   |   task_service.py
|   |   |   user_service.py
|   |   |   __init__.py
|   |   |
|   +---utils
|   |   |   uow.py
|   |   |   websocket.py
|   |   |   __init__.py
|   |   |
+---tests
|   |   auth_test.py
|   |   conftest.py
|   |   docker-compose.yml
|   |   errors.py
|   |   tasks_test.py
|   .gitattributes
|   .gitignore
|   alembic.ini
|   docker-compose.yml
|   Dockerfile
|   logfile.log
|   pyproject.toml
|   README.md
|   requirements.txt
```
