### Примеры запросов к HTTP-сервису на Flask

#### 1. Создание позитивных отзывов
**Запрос:**
```bash
curl -X POST localhost:5000/reviews \
  -H "Content-Type: application/json" \
  -d '{"text":"Хороший сервис"}'
```

**Ответ:**
```json
{
    "id": 1,
    "text": "Хороший сервис",
    "sentiment": "positive",
    "created_at": "2025-07-17T00:07:00.123428"
}
```

---

**Запрос:**
```bash
curl -X POST localhost:5000/reviews \
  -H "Content-Type: application/json" \
  -d '{"text":"Люблю этот сервис"}'
```

**Ответ:**
```json
{
    "id": 2,
    "text": "Люблю этот сервис",
    "sentiment": "positive",
    "created_at": "2025-07-17T00:07:14.415960"
}
```

---

#### 2. Создание негативных отзывов
**Запрос:**
```bash
curl -X POST localhost:5000/reviews \
  -H "Content-Type: application/json" \
  -d '{"text":"Плохой сервис"}'
```

**Ответ:**
```json
{
    "id": 3,
    "text": "Плохой сервис",
    "sentiment": "negative",
    "created_at": "2025-07-17T00:07:30.583834"
}
```

---

**Запрос:**
```bash
curl -X POST localhost:5000/reviews \
  -H "Content-Type: application/json" \
  -d '{"text":"Ненавижу этот сервис"}'
```

**Ответ:**
```json
{
    "id": 4,
    "text": "Ненавижу этот сервис",
    "sentiment": "negative",
    "created_at": "2025-07-17T00:07:45.865089"
}
```

---

#### 3. Создание нейтрального отзыва
**Запрос:**
```bash
curl -X POST localhost:5000/reviews \
  -H "Content-Type: application/json" \
  -d '{"text":"Нормальный сервис"}'
```

**Ответ:**
```json
{
    "id": 5,
    "text": "Нормальный сервис",
    "sentiment": "neutral",
    "created_at": "2025-07-17T00:08:17.999557"
}
```

---

#### 4. Получение всех отзывов
**Запрос:**
```bash
curl "localhost:5000/reviews"
```

**Ответ:**
```json
[
    {
        "id": 1,
        "text": "Хороший сервис",
        "sentiment": "positive",
        "created_at": "2025-07-17T00:07:00.123428"
    },
    {
        "id": 2,
        "text": "Люблю этот сервис",
        "sentiment": "positive",
        "created_at": "2025-07-17T00:07:14.415960"
    },
    {
        "id": 3,
        "text": "Плохой сервис",
        "sentiment": "negative",
        "created_at": "2025-07-17T00:07:30.583834"
    },
    {
        "id": 4,
        "text": "Ненавижу этот сервис",
        "sentiment": "negative",
        "created_at": "2025-07-17T00:07:45.865089"
    },
    {
        "id": 5,
        "text": "Нормальный сервис",
        "sentiment": "neutral",
        "created_at": "2025-07-17T00:08:17.999557"
    }
]
```

---

#### 5. Фильтрация по негативным отзывам
**Запрос:**
```bash
curl "localhost:5000/reviews?sentiment=negative"
```

**Ответ:**
```json
[
    {
        "id": 3,
        "text": "Плохой сервис",
        "sentiment": "negative",
        "created_at": "2025-07-17T00:07:30.583834"
    },
    {
        "id": 4,
        "text": "Ненавижу этот сервис",
        "sentiment": "negative",
        "created_at": "2025-07-17T00:07:45.865089"
    }
]
```

---

#### 6. Обработка исключений
**Запрос (отсутствует текст):**
```bash
curl -X POST localhost:5000/reviews \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Ответ:**
```json
{
    "error": "Отсутствует переменная 'text'"
}
```