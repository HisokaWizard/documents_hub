# AGENTS.md — Documents Hub

## Промпт для агентов

Ты работаешь в репозитории технической документации. Этот репозиторий содержит **главный технологический стек** проекта — строго придерживайся описанных паттернов и технологий. НЕ предлагай альтернативные технологии или подходы, отличные от описанных в документации.

## Структура репозитория

```
documents_hub/
├── backend/               # Backend (NestJS + PostgreSQL)
│   ├── BE_APP_SETTINGS.md           ⬅️ ВХОДНАЯ ТОЧКА
│   ├── BACKEND_TESTING.md
│   ├── DATABASE.md
│   ├── MIGRATIONS.md
│   └── nestjs/            # Детальные паттерны NestJS
├── frontend/              # Frontend (React + FSD)
│   ├── FE_APP_SETTINGS.md           ⬅️ ВХОДНАЯ ТОЧКА
│   ├── TYPESCRIPT.md
│   ├── REACT.md
│   ├── REDUX.md
│   ├── ROUTING.md
│   ├── MUI.md
│   ├── FSD.md
│   ├── WEBPACK.md
│   └── TESTING.md
├── testing/               # TDD и общие правила
│   └── TESTING_RULES.md             ⬅️ ВХОДНАЯ ТОЧКА
└── opencode/              # Документация OpenCode
```

## Входные точки (главный стек)

| Раздел | Файл | Технологии |
|--------|------|------------|
| **Backend** | `./backend/BE_APP_SETTINGS.md` | NestJS, TypeScript, PostgreSQL, TypeORM |
| **Frontend** | `./frontend/FE_APP_SETTINGS.md` | React 18-19, TypeScript 5+, Redux Toolkit, RTK Query, React Router 6, MUI 7, Webpack 5 |
| **Testing** | `./testing/TESTING_RULES.md` | TDD, Red-Green-Refactor, Jest, RTL, Playwright |

## Ключевые технологии (строго соблюдать)

### Backend
- **Фреймворк**: NestJS с модульной архитектурой
- **База данных**: PostgreSQL через TypeORM
- **Архитектура**: Layered (Controllers → Services → Repositories)
- **API**: REST, DTO валидация через Pipes
- **Тестирование**: Unit (Jest) + Integration (supertest)

### Frontend
- **UI библиотека**: React 18-19 (функциональные компоненты + hooks)
- **Типизация**: TypeScript 5+ (strict mode обязателен)
- **Состояние**: Redux Toolkit + RTK Query
- **Роутинг**: React Router 6
- **UI компоненты**: MUI 7 (Material UI)
- **Сборка**: Webpack 5
- **Архитектура**: Feature-Sliced Design (FSD)
- **Тестирование**: Jest + React Testing Library + Playwright

### Testing (обязательно для всех)
- **Подход**: TDD — сначала тест, потом код
- **Цикл**: Red → Green → Refactor
- **Структура теста**: AAA (Arrange-Act-Assert)

## Команды

```bash
# Проверка markdown
npx markdownlint-cli "*.md"
npx markdown-link-check "*.md"
```

## Конвенции документации

### Формат
- **Язык**: Русский или английский (консистентно в документе)
- **Формат**: Markdown с mermaid-диаграммами
- **TOC**: Обязателен для документов >50 строк
- **Примеры**: Реальный код из проектов

### Структура документа
```markdown
# Заголовок

## Содержание
1. [Раздел](#раздел)

---

## Раздел
```

### Code blocks
Всегда указывать язык:
```typescript
const example = "code";
```

## Правила работы агента

1. **Читай входные точки** перед работой с кодом
2. **Строго следуй стеку** — не предлагай альтернативы
3. **Обновляй TOC** при изменении структуры документа
4. **Не дублируй** — ссылайся на существующие разделы
5. **TDD обязателен** — сначала тест, потом реализация
6. **FSD для frontend** — соблюдай слои: app, pages, widgets, features, entities, shared
7. **Layered для backend** — контроллеры → сервисы → репозитории
