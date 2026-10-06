# Домашнє завдання #8 — MongoDB, Redis, RabbitMQ

## Підготовка

```bash
pip install -r requirements.txt
cp .env.example .env          # вписати рядок підключення до MongoDB Atlas у MONGO_URI
docker compose up -d          # Redis + RabbitMQ (UI: http://localhost:15672, guest/guest)
```

Без Atlas можна підняти локальну MongoDB: `docker compose --profile local-mongo up -d`
і вказати `MONGO_URI=mongodb://localhost:27017` (або не створювати `.env` взагалі, це значення за замовчуванням).

Усі скрипти запускаються з кореня проєкту через `python -m ...`.

## Частина 1 — цитати

| Файл | Призначення |
|---|---|
| `part1/models.py` | Моделі `Author` і `Quote` (колекції `authors`, `quotes`); `Quote.author` — `ReferenceField` (зберігає `ObjectId` автора) |
| `part1/seed.py` | Завантаження `part1/data/authors.json` і `quotes.json` у базу |
| `part1/search.py` | Інтерактивний пошук цитат |

```bash
python -m part1.seed
python -m part1.search
```

Команди:

- `name: Steve Martin` або скорочено `name:st` — цитати автора (пошук за початком імені, без урахування регістру);
- `tag:life` або `tag:li` — цитати з тегом (за початком тегу);
- `tags:life,live` — цитати, що мають хоча б один із тегів;
- `exit` — вихід.

Результати `name:` і `tag:` кешуються в Redis (ключ `quotes:<команда>:<значення>`, TTL з `CACHE_TTL`);
повторний запит виводить позначку `(from cache)`. Якщо Redis недоступний — скрипт працює без кешу.
Виведення — у `utf-8`.

## Частина 2 — розсилка через RabbitMQ

| Файл | Призначення |
|---|---|
| `part2/models.py` | Модель `Contact`: `fullname`, `email`, `phone`, `preferred_method` (`email`/`sms`), `sent` (`False` за замовчуванням), `address`, `company`, `created_at`, `sent_at` |
| `part2/producer.py` | Генерує фейкові контакти (Faker), зберігає їх і кладе `ObjectId` у чергу `email_queue` або `sms_queue` залежно від `preferred_method` |
| `part2/consumer_email.py` | Обробляє `email_queue` |
| `part2/consumer_sms.py` | Обробляє `sms_queue` |
| `part2/consumer.py` | Обробляє обидві черги в одному процесі |
| `part2/worker.py` | Спільна логіка: функції-заглушки `send_email` / `send_sms`, оновлення `sent=True` |

```bash
python -m part2.consumer_email     # у першому терміналі
python -m part2.consumer_sms       # у другому
python -m part2.producer 20        # згенерувати 20 контактів
```

Черги durable, повідомлення persistent, підтвердження (`ack`) — після оновлення контакту,
тому повідомлення не губляться, якщо consumer впаде під час обробки.
