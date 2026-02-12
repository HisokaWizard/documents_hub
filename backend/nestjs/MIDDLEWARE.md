# Middleware

## Содержание

1. [Что такое Middleware](#что-такое-middleware)
2. [Назначение](#назначение)
3. [Базовый синтаксис](#базовый-синтаксис)
4. [Практические примеры](#практические-примеры)
5. [Best Practices](#best-practices)
6. [Смотрите также](#смотрите-также)

---

## Что такое Middleware

Middleware — функция, выполняющаяся до обработки запроса роутером. Имеет доступ к объектам `request` и `response`, а также к функции `next()` для передачи управления следующему middleware.

## Назначение

- **Request logging** — логирование всех входящих запросов
- **CORS handling** — управление cross-origin запросами
- **Body parsing** — парсинг JSON, URL-encoded данных
- **Authentication** — проверка токенов до попадания в guards
- **Cookie parsing** — извлечение cookies из заголовков
- **Compression** — сжатие ответов

## Базовый синтаксис

```typescript
// Классовый middleware
@Injectable()
export class LoggerMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    console.log(`Request...`);
    next();
  }
}

// Функциональный middleware
export function logger(req: Request, res: Response, next: NextFunction) {
  console.log(`Request...`);
  next();
}
```

## Практические примеры

### Logger Middleware
```typescript
@Injectable()
export class LoggerMiddleware implements NestMiddleware {
  private logger = new Logger('HTTP');

  use(req: Request, res: Response, next: NextFunction) {
    const { ip, method, originalUrl } = req;
    const userAgent = req.get('user-agent') || '';

    res.on('finish', () => {
      const { statusCode } = res;
      const contentLength = res.get('content-length');
      
      this.logger.log(
        `${method} ${originalUrl} ${statusCode} ${contentLength} - ${userAgent} ${ip}`,
      );
    });

    next();
  }
}
```

### CORS Middleware
```typescript
// Использование express cors
app.enableCors({
  origin: ['http://localhost:3000', 'https://example.com'],
  methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
  credentials: true,
});
```

### Authentication Middleware
```typescript
@Injectable()
export class AuthMiddleware implements NestMiddleware {
  constructor(private jwtService: JwtService) {}

  async use(req: Request, res: Response, next: NextFunction) {
    const authHeader = req.headers.authorization;
    
    if (!authHeader) {
      return next();
    }

    const [type, token] = authHeader.split(' ');
    
    if (type === 'Bearer' && token) {
      try {
        const payload = await this.jwtService.verifyAsync(token);
        req.user = payload;
      } catch {
        // Token invalid, continue without user
      }
    }
    
    next();
  }
}
```

### Conditional middleware
```typescript
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer
      .apply(LoggerMiddleware)
      .forRoutes({ path: 'users', method: RequestMethod.GET });
    
    consumer
      .apply(AuthMiddleware)
      .exclude({ path: 'auth/login', method: RequestMethod.POST })
      .forRoutes('*');
  }
}
```

### Multiple middleware
```typescript
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer
      .apply(cors(), helmet(), compression())
      .forRoutes('*');
  }
}
```

### Global middleware
```typescript
// В main.ts
app.use(logger);

// Или
app.use((req, res, next) => {
  console.log('Global middleware');
  next();
});
```

## Middleware vs Guards vs Interceptors

| Aspect | Middleware | Guards | Interceptors |
|--------|-----------|---------|--------------|
| **When** | Before routing | After routing, before handler | Around handler |
| **Access** | req/res | ExecutionContext | ExecutionContext |
| **Use case** | Pre-processing | Authorization | Post-processing |
| **Scope** | Route/path based | Controller/method | Controller/method |

## Best Practices

- **Order matters** — middleware выполняется в порядке регистрации
- **Functional for simple** — используйте функции для простой логики
- **Class for DI** — классы для middleware с зависимостями
- **Global for common** — глобальные middleware для общих задач
- **Avoid business logic** — middleware только для infrastructure

## Смотрите также

- [GUARD.md](./GUARD.md) — Авторизация (альтернатива для auth)
- [INTERCEPTOR.md](./INTERCEPTOR.md) — Перехват ответов
- [CONTROLLER.md](./CONTROLLER.md) — Обработка запросов
- [NEST_JS_ARCHITECTURE.md](./NEST_JS_ARCHITECTURE.md) — Общая архитектура
