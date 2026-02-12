# Exception Filter

## Содержание

1. [Что такое Exception Filter](#что-такое-exception-filter)
2. [Назначение](#назначение)
3. [Базовый синтаксис](#базовый-синтаксис)
4. [Практические примеры](#практические-примеры)
5. [Best Practices](#best-practices)
6. [Смотрите также](#смотрите-также)

---

## Что такое Exception Filter

Exception Filter перехватывает необработанные исключения и формирует понятный HTTP ответ клиенту. Позволяет централизованно управлять ошибками приложения.

## Назначение

- **Error handling** — централизованная обработка ошибок
- **Response formatting** — стандартизация формата ошибок
- **Logging** — логирование исключений
- **Exception mapping** — преобразование одних ошибок в другие
- **Client-friendly** — понятные сообщения об ошибках

## Базовый синтаксис

```typescript
@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse();
    const request = ctx.getRequest();
    const status = exception.getStatus();

    response.status(status).json({
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
    });
  }
}

@Controller('users')
@UseFilters(HttpExceptionFilter)
export class UsersController {}
```

## Практические примеры

### All Exceptions Filter
```typescript
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  private readonly logger = new Logger(AllExceptionsFilter.name);

  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse();
    const request = ctx.getRequest();

    const status = exception instanceof HttpException
      ? exception.getStatus()
      : HttpStatus.INTERNAL_SERVER_ERROR;

    const message = exception instanceof HttpException
      ? exception.getResponse()
      : 'Internal server error';

    this.logger.error(
      `${request.method} ${request.url}`,
      exception instanceof Error ? exception.stack : '',
    );

    response.status(status).json({
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
      message,
    });
  }
}
```

### Validation Exception Filter
```typescript
@Catch(BadRequestException)
export class ValidationExceptionFilter implements ExceptionFilter {
  catch(exception: BadRequestException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse();
    const status = exception.getStatus();
    const exceptionResponse = exception.getResponse() as any;

    const errors = Array.isArray(exceptionResponse.message)
      ? exceptionResponse.message
      : [exceptionResponse.message];

    response.status(status).json({
      statusCode: status,
      message: 'Validation failed',
      errors,
      timestamp: new Date().toISOString(),
    });
  }
}
```

### Database Exception Filter
```typescript
@Catch(QueryFailedError)
export class DatabaseExceptionFilter implements ExceptionFilter {
  catch(exception: QueryFailedError, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse();

    let message = 'Database error';
    let status = HttpStatus.INTERNAL_SERVER_ERROR;

    if (exception.message.includes('unique constraint')) {
      message = 'Duplicate entry';
      status = HttpStatus.CONFLICT;
    }

    response.status(status).json({
      statusCode: status,
      message,
      error: 'Database Error',
    });
  }
}
```

### Custom Exception Classes
```typescript
export class UserNotFoundException extends HttpException {
  constructor(userId: string) {
    super(`User with ID ${userId} not found`, HttpStatus.NOT_FOUND);
  }
}

export class EmailAlreadyExistsException extends HttpException {
  constructor() {
    super('Email already exists', HttpStatus.CONFLICT);
  }
}

// Использование
@Get(':id')
async findOne(@Param('id') id: string) {
  const user = await this.usersService.findOne(id);
  if (!user) {
    throw new UserNotFoundException(id);
  }
  return user;
}
```

### Global Exception Filter
```typescript
// В main.ts
app.useGlobalFilters(new AllExceptionsFilter());

// Или в модуле
providers: [
  {
    provide: APP_FILTER,
    useClass: AllExceptionsFilter,
  },
]
```

## Built-in HTTP Exceptions

```typescript
// 4xx Client Errors
throw new BadRequestException();           // 400
throw new UnauthorizedException();         // 401
throw new ForbiddenException();            // 403
throw new NotFoundException();             // 404
throw new ConflictException();             // 409
throw new UnprocessableEntityException();  // 422

// 5xx Server Errors
throw new InternalServerErrorException();  // 500
throw new BadGatewayException();           // 502
throw new ServiceUnavailableException();   // 503
```

## Best Practices

- **Catch all** — всегда имейте fallback filter для неожиданных ошибок
- **Don't expose internals** — не отправляйте stack traces клиенту в production
- **Structured errors** — используйте единый формат ошибок
- **Log properly** — логируйте ошибки с контекстом
- **Custom exceptions** — создавайте специфические исключения для домена

## Смотрите также

- [PIPE.md](./PIPE.md) — Валидация входных данных
- [CONTROLLER.md](./CONTROLLER.md) — Выброс исключений
- [NEST_JS_ARCHITECTURE.md](./NEST_JS_ARCHITECTURE.md) — Общая архитектура
