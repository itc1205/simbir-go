# Simbir GO - Проект для VolgaIT

## Описание проекта

Цель: Создать backend часть сервиса по аренде автомобилей

Инструменты, используемые при создании проекта:
1. Python 3.11
2. Docker
3. PostgreSQL

Фреймворки:
1. FastAPI
2. SQLAlchemy
3. Pydantic

## Инструкции по запуску, управлению

Если установлен Docker и Make

```bash
make build # Для сборки проекта
make up # Для запуска проекта
make down # Для выключения проекта
```

Если установлен только Docker

```bash
docker-compose build  # Для сборки проекта
docker-compose up -d  # Для запуска проекта
docker-compose down --remove-orphans # Для остановки проекта
docker-compose logs --tail=25 api    # Для просмотра логов
```

Если нет ничего

Предполагается что PostgreSQL уже доступен по адресу postgresql://localhost:54321, и пользователь с логином **simbir_go** и паролем **sOm_e_dum8_p*ssw0|^d** уже существует. Иначе воспользуйтесь переменными среды DB_HOST, DB_PASSWORD и DB_USER соответственно

```bash
python -m venv .venv # Создайте виртуальную среду в папке .venv
# Далее активируйте виртуальную среду для вашего шелла
pip install -r ./requirements.txt
pip install -e /src
uvicorn simbir_go_backend.entrypoint.fastapi_app:app --host=0.0.0.0 --port=80
```

## Swagger

Находится в <host>:<port>/docs

Дефолтный админ:
username: admin
password: admin

либо то, что указано в переменных среды DEFAULT_ADMIN DEFAULT_PASSWORD *(для докера это just_admin и just_password)*

## Redoc

Находится в <host>:<port>/redoc