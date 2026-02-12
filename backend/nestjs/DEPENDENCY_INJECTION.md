# Dependency Injection

## Содержание

1. [Что такое Dependency Injection](#что-такое-dependency-injection)
2. [Назначение](#назначение)
3. [Базовый синтаксис](#базовый-синтаксис)
4. [Практические примеры](#практические-примеры)
5. [Best Practices](#best-practices)
6. [Смотрите также](#смотрите-также)

---

## Что такое Dependency Injection

Dependency Injection (DI) — паттерн проектирования, при котором зависимости компонентов предоставляются извне, а не создаются внутри. NestJS использует собственный DI контейнер.

## Назначение

- **Loose coupling** — слабая связанность компонентов
- **Testability** — легкое мокирование зависимостей
- **Flexibility** — возможность замены реализаций
- **Reusability** — переиспользование компонентов
- **Maintainability** — упрощение поддержки кода

## Базовый синтаксис

```typescript
// Определение сервиса
@Injectable()
export class UsersService {
  constructor(private readonly repository: UsersRepository) {}
}

// Внедрение в контроллер
@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}
}
```

## Практические примеры

### Constructor injection
```typescript
@Injectable()
export class AuthService {
  constructor(
    private readonly usersService: UsersService,
    private readonly jwtService: JwtService,
  ) {}
}
```

### Property injection (реже)
```typescript
@Injectable()
export class MyService {
  @Inject('CONFIG')
  private readonly config: Config;
}
```

### Provider tokens
```typescript
@Injectable()
export class DatabaseService {
  constructor(@Inject('DATABASE_CONNECTION') private connection: Connection) {}
}

// В модуле
providers: [
  { provide: 'DATABASE_CONNECTION', useValue: connection },
]
```

### useClass provider
```typescript
providers: [
  { provide: UsersService, useClass: MockUsersService },
]
```

### useFactory provider
```typescript
providers: [
  {
    provide: 'CONFIG',
    useFactory: () => process.env.NODE_ENV === 'production' ? prodConfig : devConfig,
  },
]
```

### useValue provider
```typescript
providers: [
  { provide: 'API_KEY', useValue: 'secret-key-123' },
]
```

### Circular dependency
```typescript
@Injectable()
export class UsersService {
  constructor(@Inject(forwardRef(() => AuthService)) private authService: AuthService) {}
}
```

### Optional injection
```typescript
@Injectable()
export class MyService {
  constructor(@Optional() private readonly optionalService?: OptionalService) {}
}
```

## Best Practices

- **Constructor injection** — предпочитайте конструктор внедрению свойств
- **Explicit dependencies** — явно объявляйте типы
- **Interface-based** — используйте интерфейсы для абстракций
- **Avoid circular deps** — рефакторите код для устранения циклов
- **Token naming** — используйте константы для provider tokens

## Смотрите также

- [SERVICE.md](./SERVICE.md) — Создание сервисов
- [MODULE.md](./MODULE.md) — Регистрация провайдеров
- [NEST_JS_ARCHITECTURE.md](./NEST_JS_ARCHITECTURE.md) — Общая архитектура
