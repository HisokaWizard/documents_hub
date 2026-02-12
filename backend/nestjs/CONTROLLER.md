# Controller

## Содержание

1. [Что такое Controller](#что-такое-controller)
2. [Назначение](#назначение)
3. [Базовый синтаксис](#базовый-синтаксис)
4. [Практические примеры](#практические-примеры)
5. [Best Practices](#best-practices)
6. [Смотрите также](#смотрите-также)

---

## Что такое Controller

Controller отвечает за обработку входящих HTTP запросов и возвращение ответов клиенту. Определяет маршруты и привязывает их к методам класса.

## Назначение

- **Routing** — определение URL endpoints
- **Request handling** — обработка HTTP методов (GET, POST, PUT, DELETE)
- **Input extraction** — получение данных из запроса (body, params, query)
- **Response formation** — формирование HTTP ответов
- **Delegation** — делегирование бизнес-логики сервисам

## Базовый синтаксис

```typescript
@Controller('users')
export class UsersController {
  @Get()
  findAll() {
    return this.usersService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.usersService.findOne(id);
  }

  @Post()
  create(@Body() createUserDto: CreateUserDto) {
    return this.usersService.create(createUserDto);
  }
}
```

## Практические примеры

### Route parameters
```typescript
@Get(':id')
findOne(@Param('id') id: string) {}

@Get(':id/posts/:postId')
getPost(@Param() params: { id: string; postId: string }) {}
```

### Query parameters
```typescript
@Get()
findAll(@Query('page') page: number, @Query('limit') limit: number) {}

@Get()
findAll(@Query() query: PaginationDto) {}
```

### Request body
```typescript
@Post()
@HttpCode(201)
create(@Body() createUserDto: CreateUserDto) {}

@Put(':id')
update(@Param('id') id: string, @Body() updateUserDto: UpdateUserDto) {}
```

### Headers and Cookies
```typescript
@Get()
findAll(@Headers('authorization') auth: string) {}

@Get()
findAll(@Req() req: Request) {
  const token = req.cookies['token'];
}
```

### Async controllers
```typescript
@Get()
async findAll(): Promise<User[]> {
  return await this.usersService.findAll();
}
```

### Response manipulation
```typescript
@Get()
@Redirect('https://example.com', 301)
redirect() {}

@Get()
@Header('Cache-Control', 'none')
getData() {}
```

## Best Practices

- **Thin controllers** — минимум логики, делегируйте сервисам
- **DTO validation** — используйте Pipes для валидации входных данных
- **Consistent naming** — методы в соответствии с действием (find, create, update, remove)
- **Status codes** — явно указывайте @HttpCode для non-200 ответов
- **Route nesting** — используйте вложенность для связанных ресурсов

## Смотрите также

- [MODULE.md](./MODULE.md) — Организация модулей
- [SERVICE.md](./SERVICE.md) — Бизнес-логика
- [PIPE.md](./PIPE.md) — Валидация данных
- [GUARD.md](./GUARD.md) — Авторизация
- [NEST_JS_ARCHITECTURE.md](./NEST_JS_ARCHITECTURE.md) — Общая архитектура
