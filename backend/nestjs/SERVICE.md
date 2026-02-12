# Service

## Содержание

1. [Что такое Service](#что-такое-service)
2. [Назначение](#назначение)
3. [Базовый синтаксис](#базовый-синтаксис)
4. [Практические примеры](#практические-примеры)
5. [Best Practices](#best-practices)
6. [Смотрите также](#смотрите-также)

---

## Что такое Service

Service (или Provider) — это класс с бизнес-логикой приложения. Помечается декоратором `@Injectable()` и может быть внедрён в другие компоненты через Dependency Injection.

## Назначение

- **Business logic** — реализация бизнес-правил
- **Data processing** — обработка и трансформация данных
- **Reusability** — переиспользование логики между контроллерами
- **Testability** — изоляция логики для unit-тестирования
- **Separation of concerns** — отделение HTTP слоя от бизнес-логики

## Базовый синтаксис

```typescript
@Injectable()
export class UsersService {
  constructor(private readonly usersRepository: UsersRepository) {}

  async findAll(): Promise<User[]> {
    return this.usersRepository.find();
  }

  async create(createUserDto: CreateUserDto): Promise<User> {
    const user = new User(createUserDto);
    return this.usersRepository.save(user);
  }
}
```

## Практические примеры

### CRUD сервис
```typescript
@Injectable()
export class UsersService {
  findAll() {}
  findOne(id: string) {}
  create(dto: CreateUserDto) {}
  update(id: string, dto: UpdateUserDto) {}
  remove(id: string) {}
}
```

### Инъекция зависимостей
```typescript
@Injectable()
export class AuthService {
  constructor(
    private readonly usersService: UsersService,
    private readonly jwtService: JwtService,
    private readonly configService: ConfigService,
  ) {}
}
```

### Custom provider
```typescript
@Injectable()
export class LoggerService {
  private readonly logger = new Logger('App');
  
  log(message: string) {
    this.logger.log(message);
  }
}
```

### Factory provider
```typescript
@Injectable()
export class DatabaseService {
  constructor(@Inject('DB_CONFIG') private config: DbConfig) {}
}

// В модуле
providers: [
  {
    provide: 'DB_CONFIG',
    useFactory: (config: ConfigService) => config.get('database'),
    inject: [ConfigService],
  },
]
```

### Scoped providers
```typescript
@Injectable({ scope: Scope.REQUEST })
export class RequestService {
  constructor(@Inject(REQUEST) private request: Request) {}
}

@Injectable({ scope: Scope.TRANSIENT })
export class TransientService {}
```

## Best Practices

- **Single Responsibility** — один сервис = один домен
- **Dependency injection** — внедряйте зависимости через constructor
- **Async/await** — используйте для асинхронных операций
- **Error handling** — выбрасывайте специфические exceptions
- **No HTTP logic** — не используйте @Req, @Res в сервисах

## Смотрите также

- [DEPENDENCY_INJECTION.md](./DEPENDENCY_INJECTION.md) — DI паттерн
- [MODULE.md](./MODULE.md) — Регистрация провайдеров
- [CONTROLLER.md](./CONTROLLER.md) — Использование сервисов
- [REPOSITORY.md](./REPOSITORY.md) — Доступ к данным
- [NEST_JS_ARCHITECTURE.md](./NEST_JS_ARCHITECTURE.md) — Общая архитектура
