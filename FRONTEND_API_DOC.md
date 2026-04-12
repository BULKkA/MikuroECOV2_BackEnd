# Mikuro Blog Backend API (Frontend Documentation)

Документация предназначена для фронтенд-реализации. Все эндпоинты находятся по базовому URL `http://localhost:8000`.

## Общие правила

- Все защищённые (auth-required) запросы должны отправляться с заголовком `Authorization: Bearer <access_token>`.
- Формат запроса/ответа: JSON.
- Ошибки приходят как `{ "detail": "..." }`.

---

## 1) Auth

### POST /api/auth/register

- Описание: регистрация нового пользователя
- Тело:
  - email: string
  - password: string
  - name: string
  - avatar_url: string|null

Пример:
```json
{
  "email": "test@example.com",
  "password": "password123",
  "name": "Test User",
  "avatar_url": null
}
```

- Успех (200):
```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

### POST /api/auth/login

- Описание : логин пользователя
- Тело:
  - email
  - password

Успех:
```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

### POST /api/auth/logout

- Описание: выход (заглушка, не требует тела)
- Успех:
```json
{ "message": "Successfully logged out" }
```

### GET /api/auth/me

- Описание: получить профиль текущего пользователя
- Заголовки: `Authorization`

Ответ:
```json
{
  "id": 1,
  "email": "test@example.com",
  "name": "Test User",
  "avatar_url": null,
  "role": "user|editor|admin",
  "email_verified": true,
  "created_at": "2026-...",
  "updated_at": "..."
}
```

### POST /api/auth/refresh

- Описание: обновление access token (в текущей реализации просто требует валидную сессионную авторизацию)
- Заголовки: `Authorization`

Ответ:
```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

---

## 2) Users

### GET /api/users/:id

- Описание: получение пользователя
- Заголовки: `Authorization`
- Параметр URL: `user_id`

Ответ: User schema (см. ниже).

### PUT /api/users/:id

- Описание: редактирование профиля (сам пользователь или admin)
- Тело:
  - name?: string
  - avatar_url?: string

Ответ: обновлённый User.

### GET /api/users

- Описание: admin только. Возвращает массив пользователей.
- Параметры:
  - skip (по умолчанию 0), limit (100)

### PUT /api/users/:id/role

- Описание: смена роли (admin only)
- Тело: `{ "role": "user" | "editor" | "admin" }`

---

## 3) Posts

### GET /api/posts

- Описание: получить публичные публикации (status == published)
- Параметры:
  - skip (int)
  - limit (int)
  - search (string, опционально)

Ответ: массив Post.

### GET /api/posts/:id

- Описание: получить пост по ID.

### GET /api/posts/slug/:slug

- Описание: получить пост по slug.

### POST /api/posts

- Описание: create post (roles editor/admin).
- Тело:
  - title (string, required)
  - summary (string|null)
  - body (string, required)
  - slug (string, required)
  - markdown (boolean, default false)
  - media (array of strings, optional)

Ответ: созданный Post (status=draft).

### PUT /api/posts/:id

- Описание: редактирование поста (author или admin).
- Тело: частичное, поля те же что для PostCreate + status.

### DELETE /api/posts/:id

- Описание: удаление поста (author или admin)

### PATCH /api/posts/:id/publish

- Описание: перевод поста в статус published (admin only)

---

## 4) Comments

### GET /api/posts/:postId/comments

- Описание: получить комментарии для поста.

### POST /api/posts/:postId/comments

- Описание: добавить комментарий (auth required)
- Тело:
  - body: string
  - parent_id: int|null

Ответ: созданный Comment.

### PUT /api/comments/:id

- Описание: редактирование комментария (author/admin)
- Тело:
  - body: string

### DELETE /api/comments/:id

- Описание: удалить комментарий (author/admin)

---

## 5) Reactions

### GET /api/reactions/posts/:postId/reactions

- Описание: получить реакции поста

### POST /api/reactions/posts/:postId/reactions

- Описание: добавить/обновить реакцию
- Тело:
  - type: "like" | "love" | "dislike"

Ответ: Reaction.

### DELETE /api/reactions/posts/:postId/reactions

- Описание: удалить реакцию текущего пользователя

---

## 6) Media

### POST /api/media/upload

- Описание: загрузка файла (editor/admin)
- Тип: multipart/form-data
- Поле: `file`

Ответ:
```json
{
  "id": "<uuid>.<ext>",
  "url": "/api/media/<id>"
}
```

### GET /api/media/:id

- Описание: скачивание/просмотр файла

---

## 7) Captcha

### POST /api/captcha/verify

- Тело: `{ "token": "..." }`
- Ответ: `{ "verified": true|false }`

---

## Схемы данных

### User
```json
{
  "id": 1,
  "email": "...",
  "name": "...",
  "avatar_url": null,
  "role": "user|editor|admin",
  "email_verified": true,
  "created_at": "...",
  "updated_at": "..."
}
```

### Post
```json
{
  "id": 1,
  "author_id": 1,
  "title": "...",
  "summary": "...",
  "body": "...",
  "slug": "...",
  "markdown": false,
  "media": null,
  "status": "draft|published",
  "created_at": "...",
  "updated_at": "...",
  "author": { ...User... }
}
```

### Comment
```json
{
  "id": 1,
  "post_id": 1,
  "author_id": 1,
  "body": "...",
  "parent_id": null,
  "created_at": "...",
  "updated_at": "...",
  "author": { ...User... }
}
```

### Reaction
```json
{
  "id": 1,
  "post_id": 1,
  "user_id": 1,
  "type": "like|love|dislike",
  "created_at": "...",
  "user": { ...User... }
}
```
