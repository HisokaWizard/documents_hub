# Pipe

## Содержание

1. [Что такое Pipe](#что-такое-pipe)
2. [Назначение](#назначение)
3. [Базовый синтаксис](#базовый-синтаксис)
4. [Практические примеры](#практические-примеры)
5. [Best Practices](#best-practices)
6. [Смотрите также](#смотрите-также)

---

## Что такое Pipe

Pipe — компонент для трансформации входных данных и выполнения валидации. Обрабатывает данные из @Body(), @Param(), @Query() перед попаданием в контроллер.

## Назначение

- **Validation** — проверка корректности входных данных
- **Transformation** — преобразование типов данных
- **Sanitization** — очистка входных данных
- **DTO enforcement** — приведение к типу DTO
- **Error handling** — ранняя валидация с понятными ошибками

## Базовый синтаксис

```typescript
@Injectable()
export class ValidationPipe implements PipeTransform {
  transform(value: any, metadata: ArgumentMetadata) {
    // Валидация/трансформация
    return value;
  }
}

@Controller('users')
export class UsersController {
  @Post()
  @UsePipes(ValidationPipe)
  create(@Body() createUserDto: CreateUserDto) {}
}
```

## Практические примеры

### ValidationPipe
```typescript
// DTO
export class CreateUserDto {
  @IsEmail()
  email: string;

  @IsString()
  @MinLength(8)
  password: string;

  @IsOptional()
  @IsInt()
  age?: number;
}

// Глобальная настройка в main.ts
app.useGlobalPipes(new ValidationPipe({
  whitelist: true,
  forbidNonWhitelisted: true,
  transform: true,
}));
```

### ParseIntPipe
```typescript
@Get(':id')
findOne(@Param('id', ParseIntPipe) id: number) {
  // id уже number
}
```

### DefaultValuePipe
```typescript
@Get()
findAll(
  @Query('page', new DefaultValuePipe(1), ParseIntPipe) page: number,
  @Query('limit', new DefaultValuePipe(10), ParseIntPipe) limit: number,
) {}
```

### Custom transformation pipe
```typescript
@Injectable()
export class ParseOptionalIntPipe implements PipeTransform {
  transform(value: string | undefined): number | undefined {
    if (value === undefined) return undefined;
    const val = parseInt(value, 10);
    if (isNaN(val)) {
      throw new BadRequestException('Validation failed');
    }
    return val;
  }
}

@Get()
findAll(@Query('age', ParseOptionalIntPipe) age?: number) {}
```

### Array validation
```typescript
export class CreateOrderDto {
  @IsArray()
  @ValidateNested({ each: true })
  @Type(() => OrderItemDto)
  items: OrderItemDto[];
}
```

### Custom validation decorator
```typescript
@ValidatorConstraint({ async: true })
export class IsUserAlreadyExistConstraint implements ValidatorConstraintInterface {
  constructor(private usersService: UsersService) {}

  async validate(email: string) {
    const user = await this.usersService.findByEmail(email);
    return !user;
  }

  defaultMessage() {
    return 'User with this email already exists';
  }
}

export function IsUserAlreadyExist(validationOptions?: ValidationOptions) {
  return function (object: object, propertyName: string) {
    registerDecorator({
      target: object.constructor,
      propertyName: propertyName,
      options: validationOptions,
      constraints: [],
      validator: IsUserAlreadyExistConstraint,
    });
  };
}
```

## Best Practices

- **Global validation** — используйте ValidationPipe глобально
- **whitelist** — удаляйте неожиданные поля из входных данных
- **transform** — автоматически преобразуйте plain objects в классы
- **DTO validation** — валидируйте все входные данные через DTO
- **Custom messages** — предоставляйте понятные сообщения об ошибках

## Смотрите также

- [CONTROLLER.md](./CONTROLLER.md) — Использование pipes
- [DECORATOR.md](./DECORATOR.md) — Создание валидаторов
- [EXCEPTION_FILTER.md](./EXCEPTION_FILTER.md) — Обработка ошибок валидации
- [NEST_JS_ARCHITECTURE.md](./NEST_JS_ARCHITECTURE.md) — Общая архитектура
