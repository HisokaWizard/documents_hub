# Interceptor

## Содержание

1. [Что такое Interceptor](#что-такое-interceptor)
2. [Назначение](#назначение)
3. [Базовый синтаксис](#базовый-синтаксис)
4. [Практические примеры](#практические-примеры)
5. [Best Practices](#best-practices)
6. [Смотрите также](#смотрите-также)

---

## Что такое Interceptor

Interceptor перехватывает входящие запросы и исходящие ответы, позволяя выполнять дополнительную логику до и после обработки запроса контроллером.

## Назначение

- **Logging** — логирование входящих запросов и ответов
- **Transformation** — трансформация ответа перед отправкой клиенту
- **Caching** — кэширование ответов
- **Error handling** — глобальная обработка ошибок
- **Timeout** — управление таймаутами
- **Exception mapping** — преобразование исключений

## Базовый синтаксис

```typescript
@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    console.log('Before...');
    
    const now = Date.now();
    return next.handle().pipe(
      tap(() => console.log(`After... ${Date.now() - now}ms`)),
    );
  }
}

@Controller('users')
@UseInterceptors(LoggingInterceptor)
export class UsersController {}
```

## Практические примеры

### Logging Interceptor
```typescript
@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  private readonly logger = new Logger('HTTP');

  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();
    const method = request.method;
    const url = request.url;
    const now = Date.now();

    return next.handle().pipe(
      tap(() => {
        this.logger.log(`${method} ${url} - ${Date.now() - now}ms`);
      }),
    );
  }
}
```

### Transform Interceptor
```typescript
@Injectable()
export class TransformInterceptor<T> implements NestInterceptor<T, Response<T>> {
  intercept(context: ExecutionContext, next: CallHandler): Observable<Response<T>> {
    return next.handle().pipe(
      map(data => ({
        data,
        statusCode: context.switchToHttp().getResponse().statusCode,
        timestamp: new Date().toISOString(),
      })),
    );
  }
}

interface Response<T> {
  data: T;
  statusCode: number;
  timestamp: string;
}
```

### Errors Interceptor
```typescript
@Injectable()
export class ErrorsInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    return next.handle().pipe(
      catchError(err => throwError(() => new BadGatewayException())),
    );
  }
}
```

### Cache Interceptor
```typescript
@Injectable()
export class CacheInterceptor implements NestInterceptor {
  private cache = new Map<string, any>();

  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const key = context.switchToHttp().getRequest().url;
    
    if (this.cache.has(key)) {
      return of(this.cache.get(key));
    }

    return next.handle().pipe(
      tap(response => this.cache.set(key, response)),
    );
  }
}
```

### Timeout Interceptor
```typescript
@Injectable()
export class TimeoutInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    return next.handle().pipe(
      timeout(5000),
      catchError(err => {
        if (err instanceof TimeoutError) {
          return throwError(() => new RequestTimeoutException());
        }
        return throwError(() => err);
      }),
    );
  }
}
```

### Global Interceptor
```typescript
// В main.ts
app.useGlobalInterceptors(new LoggingInterceptor());

// Или в модуле
providers: [
  {
    provide: APP_INTERCEPTOR,
    useClass: LoggingInterceptor,
  },
]
```

## Best Practices

- **Pure functions** — избегайте side effects
- **Error handling** — всегда обрабатывайте ошибки в pipe
- **Performance** — не блокируйте event loop
- **Global vs local** — используйте глобальные interceptors для общей логики
- **Composition** — комбинируйте через @UseInterceptors(Interceptor1, Interceptor2)

## Смотрите также

- [MIDDLEWARE.md](./MIDDLEWARE.md) — Отличия от middleware
- [CONTROLLER.md](./CONTROLLER.md) — Применение interceptors
- [GUARD.md](./GUARD.md) — Авторизация
- [NEST_JS_ARCHITECTURE.md](./NEST_JS_ARCHITECTURE.md) — Общая архитектура
