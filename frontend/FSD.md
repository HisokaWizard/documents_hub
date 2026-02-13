# FSD (Feature-Sliced Design)

## Содержание

1. [Обзор](#обзор)
2. [Слои](#слои)
3. [Сегменты](#сегменты)
4. [Публичный API](#публичный-api)
5. [Импорты](#импорты)
6. [Пример](#пример)

---

## Обзор

Feature-Sliced Design (FSD) — архитектурная методология для frontend приложений. Разбивает приложение по фичам, где каждая фича изолирована и содержит всё необходимое.

**Принципы:**
- Изоляция фич — каждая фича независима
- Single Responsibility — один модуль = одна задача
- Low Coupling — слабая связанность между модулями
- Explicit imports — явные зависимости через Public API

## Слои

```
src/
├── app/           # Инициализация приложения
├── processes/     # Бизнес-процессы (auth flow, checkout)
├── pages/         # Страницы приложения
├── widgets/       # Самостоятельные блоки UI
├── features/      # Фичи (user interactions)
├── entities/      # Бизнес-сущности
└── shared/        # Переиспользуемый код
```

**Правило:** слой может зависеть только от нижележащих слоев.

```
pages → widgets → features → entities → shared
```

## Сегменты

Каждый модуль состоит из сегментов:

```
feature/
├── ui/           # UI-компоненты
├── model/        # Бизнес-логика (store, actions)
├── api/          # API запросы
├── lib/          # Хелперы и утилиты
├── config/       # Конфигурация
└── index.ts      # Public API
```

## Публичный API

```ts
// features/auth/index.ts
export { LoginForm } from './ui/LoginForm';
export { useAuth } from './model/useAuth';
export { authSlice, authActions } from './model/authSlice';
export type { AuthState, User } from './model/types';

// Наружу экспортируется ТОЛЬКО из index.ts
// Внутренние модули не импортируются напрямую
```

## Импорты

```ts
// ✅ Правильно — через Public API
import { LoginForm } from '@/features/auth';

// ❌ Неправильно — прямой импорт
import { LoginForm } from '@/features/auth/ui/LoginForm';

// ✅ Absolute imports
import { Button } from '@/shared/ui';
import { UserCard } from '@/entities/user';

// ✅ Relative imports только внутри модуля
import { useAuth } from '../model/useAuth';
```

## Пример

```
src/
├── app/
│   ├── providers/
│   │   ├── StoreProvider.tsx
│   │   └── RouterProvider.tsx
│   ├── styles/
│   │   └── global.css
│   └── index.tsx
│
├── pages/
│   ├── home/
│   │   ├── ui/
│   │   │   └── HomePage.tsx
│   │   └── index.ts
│   └── profile/
│       ├── ui/
│       │   └── ProfilePage.tsx
│       └── index.ts
│
├── widgets/
│   └── header/
│       ├── ui/
│       │   ├── Header.tsx
│       │   └── NavMenu.tsx
│       ├── model/
│       │   └── useNavigation.ts
│       └── index.ts
│
├── features/
│   ├── auth/
│   │   ├── ui/
│   │   │   ├── LoginForm.tsx
│   │   │   └── LogoutButton.tsx
│   │   ├── model/
│   │   │   ├── authSlice.ts
│   │   │   └── useAuth.ts
│   │   ├── api/
│   │   │   └── authApi.ts
│   │   └── index.ts
│   └── create-post/
│       ├── ui/
│       │   └── CreatePostForm.tsx
│       ├── model/
│       │   └── createPostSlice.ts
│       └── index.ts
│
├── entities/
│   └── user/
│       ├── ui/
│       │   ├── UserCard.tsx
│       │   └── Avatar.tsx
│       ├── model/
│       │   ├── userSlice.ts
│       │   └── types.ts
│       └── index.ts
│
└── shared/
    ├── api/
    │   └── baseApi.ts
    ├── ui/
    │   ├── Button/
    │   ├── Input/
    │   └── Card/
    ├── lib/
    │   ├── formatDate.ts
    │   └── useDebounce.ts
    └── config/
        └── routes.ts
```

## Best Practices

```ts
// Сущность — минимальная бизнес-логика
// entities/user/model/types.ts
export interface User {
  id: string;
  email: string;
  name: string;
}

// Фича — пользовательское взаимодействие
// features/edit-profile/ui/EditProfileForm.tsx
export const EditProfileForm = () => {
  const user = useSelector(selectCurrentUser);
  const dispatch = useDispatch();
  
  const handleSubmit = (data: UserFormData) => {
    dispatch(updateUser(data));
  };
  
  return <UserForm user={user} onSubmit={handleSubmit} />;
};

// Виджет — композиция сущностей и фич
// widgets/profile-card/ui/ProfileCard.tsx
export const ProfileCard = () => {
  return (
    <Card>
      <UserCard /> {/* entity */}
      <EditProfileForm /> {/* feature */}
    </Card>
  );
};

// Страница — композиция виджетов
// pages/profile/ui/ProfilePage.tsx
export const ProfilePage = () => {
  return (
    <PageLayout>
      <Header /> {/* widget */}
      <ProfileCard /> {/* widget */}
    </PageLayout>
  );
};
```
