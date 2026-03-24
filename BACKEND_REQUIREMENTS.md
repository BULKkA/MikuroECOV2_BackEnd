# Требования к Backend для проекта MikuroECOV2

## Цель
Обеспечить надежное, масштабируемое и безопасное API для блога с регистрацией/авторизацией, ролями, постами, комментариями, реакциями и медиа.

## Архитектурные решения
- Python 3.11+
- web-фреймворк: FastAPI
- REST API (+ OpenAPI авто-документация через FastAPI)
- Базы данных: PostgreSQL / MySQL / SQLite (для локальной разработки) через SQLAlchemy/SQLModel
- Авторизация: JWT (access + refresh) через `fastapi-users` / `fastapi-jwt-auth` + refresh token через secure httpOnly cookie
- Хранение медиа: S3-совместимое хранилище, CDN, либо локальная файловая система (для прототипа)
- Migrations: Alembic
- Контейнеризация: Docker
- Конфигурация: Pydantic `BaseSettings` для переменных окружения
- Background tasks: `FastAPI BackgroundTasks` / Celery для тяжелых задач (например, отправка писем)


## Основные модели
1. Пользователь (`User`)
   - id, email, password_hash, name, avatar_url, role (`user`, `editor`, `admin`), created_at, updated_at
   - проведения подтверждения e-mail (email_verified)

2. Пост (`Post`)
   - id, author_id, title, summary, body, slug, markdown (bool), media [] (url + type), status (`draft`, `published`), created_at, updated_at

3. Комментарий (`Comment`)
   - id, post_id, author_id, body, parent_id (опционально), created_at, updated_at

4. Реакция (`Reaction`)
   - id, post_id, user_id, type (`like`, `love`, `dislike`, ...), created_at

5. Капча (`CaptchaRequest`)
   - id, token, user_ip, created_at, verified_at

## RBAC (Права)
- аутентификация: доступ к созданным ресурсам при наличии токена
- `editor` и `admin`: могут создавать посты
- `admin` + автор: могут обновлять/удалять пост
- `user`: могут комментировать, реагировать
- `guest`: только чтение публичных постов

## Эндпоинты
### Auth
- POST `/api/auth/register` (с captcha)
- POST `/api/auth/login` (с captcha)
- POST `/api/auth/logout`
- GET `/api/auth/me`
- POST `/api/auth/refresh`
- POST `/api/auth/forgot-password` (опционально)

### Users
- GET `/api/users/:id`
- PUT `/api/users/:id`
- GET `/api/users` (admin)
- PUT `/api/users/:id/role` (admin)

### Posts
- GET `/api/posts` (фильтрация, пагинация, поиск)
- GET `/api/posts/:id` или `/api/posts/slug/:slug`
- POST `/api/posts` (editor/admin)
- PUT `/api/posts/:id` (admin/author)
- DELETE `/api/posts/:id` (admin/author)
- PATCH `/api/posts/:id/publish`(admin)

### Comments
- GET `/api/posts/:postId/comments`
- POST `/api/posts/:postId/comments` (auth)
- PUT `/api/comments/:id` (author/admin)
- DELETE `/api/comments/:id` (author/admin)

### Reactions
- GET `/api/posts/:postId/reactions`
- POST `/api/posts/:postId/reactions` (auth)
- DELETE `/api/posts/:postId/reactions` (auth)

### Media
- POST `/api/media/upload` (auth, role editor/admin, max size, mime whitelist)
- GET `/api/media/:id`

### Captcha
- POST `/api/captcha/verify`

## Безопасность
- HTTPS
- валидация входных данных (schema validation)
- защита от CSRF (если cookie-based)
- rate limit на аутентификацию и форму регистрации
- хеширование паролей Argon2/Bcrypt/PBKDF2
- защита от SQL Injection/NoSQL Injection
- Content Security Policy
- sanitize markdown при рендере

## Тестирование
- Unit-тесты (Jest/Mocha/pytest)
- Интеграционные тесты (supertest, Postman/Newman)
- e2e проверки ключевых сценариев

## Логирование и мониторинг
- централизованные логи (структурированные JSON)
- прочие метрики: ошибки 5xx, логи входа, действия модерации
- оповещение при падении/ошибках

## Документация
- OpenAPI/Swagger
- Postman collection

## Расширения (будущее)
- WebSockets / сервер событий Live updates
- ML-фильтр спама/модерации
- multi-tenant / импорт/экспорт
