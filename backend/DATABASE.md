# Database (SQL)

## Содержание

1. [Реляционные базы данных](#реляционные-базы-данных)
2. [Основные концепции](#основные-концепции)
3. [SQL запросы](#sql-запросы)
4. [Нормализация](#нормализация)
5. [Индексы](#индексы)
6. [Транзакции](#транзакции)

---

## Реляционные базы данных

Реляционная БД хранит данные в таблицах со связями между ними. Каждая таблица — это набор строк (records) и столбцов (fields).

**Популярные SQL БД:**
- **PostgreSQL** — production-ready, расширяемая
- **MySQL** — широко распространена, простая
- **SQLite** — файловая БД, для малых проектов и тестов

## Основные концепции

**Таблица (Table)** — структура для хранения данных одного типа.
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Первичный ключ (Primary Key)** — уникальный идентификатор записи.
```sql
id SERIAL PRIMARY KEY
```

**Внешний ключ (Foreign Key)** — связь между таблицами.
```sql
user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
```

**Связи (Relationships):**
- One-to-One: один к одному
- One-to-Many: один ко многим
- Many-to-Many: многие ко многим (через junction table)

## SQL запросы

**CRUD операции:**
```sql
-- Create
INSERT INTO users (email, name) VALUES ('user@example.com', 'John');

-- Read
SELECT * FROM users WHERE email = 'user@example.com';
SELECT id, name FROM users ORDER BY created_at DESC LIMIT 10;

-- Update
UPDATE users SET name = 'Jane' WHERE id = 1;

-- Delete
DELETE FROM users WHERE id = 1;
```

**Join запросы:**
```sql
-- INNER JOIN
SELECT users.name, posts.title
FROM users
INNER JOIN posts ON users.id = posts.user_id;

-- LEFT JOIN (все users, даже без постов)
SELECT users.name, COUNT(posts.id) as post_count
FROM users
LEFT JOIN posts ON users.id = posts.user_id
GROUP BY users.id;
```

**Агрегатные функции:**
```sql
SELECT 
  COUNT(*) as total_users,
  AVG(age) as avg_age,
  MAX(created_at) as latest
FROM users;
```

## Нормализация

Процесс организации данных для уменьшения избыточности.

**1NF (Первая нормальная форма):**
- Атомарные значения (не списки в ячейках)
- Уникальные строки

**2NF (Вторая нормальная форма):**
- Все поля зависят от всего первичного ключа (для составных ключей)

**3NF (Третья нормальная форма):**
- Нет транзитивных зависимостей (поля зависят только от PK)

**Пример нормализации:**
```sql
-- До (не нормализовано)
CREATE TABLE orders (
  order_id INT,
  customer_name VARCHAR,
  customer_email VARCHAR,
  product_name VARCHAR,
  product_price DECIMAL
);

-- После (3NF)
CREATE TABLE customers (
  id SERIAL PRIMARY KEY,
  name VARCHAR,
  email VARCHAR UNIQUE
);

CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR,
  price DECIMAL
);

CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  customer_id INT REFERENCES customers(id),
  product_id INT REFERENCES products(id),
  quantity INT
);
```

## Индексы

Ускоряют поиск, но замедляют запись.

```sql
-- B-tree индекс (по умолчанию)
CREATE INDEX idx_users_email ON users(email);

-- Уникальный индекс
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);

-- Составной индекс
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- Индекс для LIKE '%text%'
CREATE INDEX idx_posts_content ON posts USING gin(to_tsvector('english', content));
```

**Когда создавать индексы:**
- Поля часто используются в WHERE
- Foreign keys
- Поля сортировки (ORDER BY)
- Поля поиска (LIKE, полнотекстовый поиск)

## Транзакции

Гарантируют атомарность операций.

```sql
BEGIN;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Если оба UPDATE успешны
COMMIT;

-- Если произошла ошибка
ROLLBACK;
```

**ACID свойства:**
- **Atomicity** — атомарность (всё или ничего)
- **Consistency** — согласованность (данные валидны)
- **Isolation** — изоляция (транзакции не мешают друг другу)
- **Durability** — долговечность (данные сохранены)

**Уровни изоляции:**
```sql
-- Read Uncommitted (можно видеть незафиксированные данные)
-- Read Committed (только зафиксированные) — DEFAULT
-- Repeatable Read (в рамках транзакции данные не меняются)
-- Serializable (полная изоляция)

SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```
