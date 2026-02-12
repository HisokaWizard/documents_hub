# Decorator

## Содержание

1. [Что такое Decorator](#что-такое-decorator)
2. [Назначение](#назначение)
3. [Базовый синтаксис](#базовый-синтаксис)
4. [Практические примеры](#практические-примеры)
5. [Best Practices](#best-practices)
6. [Смотрите также](#смотрите-также)

---

## Что такое Decorator

Decorator — TypeScript feature, позволяющий добавлять метаданные к классам, методам, свойствам и параметрам. В NestJS декораторы — основной механизм конфигурации.

## Назначение

- **Metadata** — добавление мета-информации к классам
- **Routing** — определение URL endpoints
- **DI marking** — маркировка инжектируемых классов
- **Validation** — декларативная валидация
- **Authorization** — указание ролей и прав
- **Transformation** — декларативное преобразование данных

## Базовый синтаксис

```typescript
// Class decorator
@Controller('users')
export class UsersController {}

// Method decorator
@Get()
findAll() {}

// Parameter decorator
@Get(':id')
findOne(@Param('id') id: string) {}

// Property decorator
@Injectable()
export class UsersService {
  @Inject('CONFIG')
  private config: Config;
}
```

## Практические примеры

### Built-in Decorators

```typescript
// Module decorators
@Module({ imports: [], controllers: [], providers: [] })
@Global()

// Controller decorators
@Controller('users')
@Get(), @Post(), @Put(), @Delete(), @Patch()
@Param(), @Query(), @Body(), @Headers()
@Req(), @Res()

// Service decorators
@Injectable()
@Inject('TOKEN')

// Guard/Interceptor/Pipe decorators
@UseGuards(AuthGuard)
@UseInterceptors(LoggingInterceptor)
@UsePipes(ValidationPipe)
@Catch(HttpException)

// Http decorators
@HttpCode(201)
@Header('Cache-Control', 'none')
@Redirect('https://example.com', 301)
```

### Custom Decorator с метаданными
```typescript
export const Roles = (...roles: Role[]) => SetMetadata('roles', roles);

// Использование
@Controller('admin')
@Roles(Role.ADMIN, Role.MODERATOR)
export class AdminController {}

// Чтение в Guard
const roles = this.reflector.get<Role[]>('roles', context.getHandler());
```

### Custom Parameter Decorator
```typescript
export const CurrentUser = createParamDecorator(
  (data: keyof User | undefined, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    const user = request.user;
    
    return data ? user?.[data] : user;
  },
);

// Использование
@Get('profile')
getProfile(@CurrentUser() user: User) {}

@Get('email')
getEmail(@CurrentUser('email') email: string) {}
```

### Custom Property Decorator
```typescript
export const Column = (options: ColumnOptions = {}): PropertyDecorator => {
  return (target: object, propertyKey: string | symbol) => {
    // Добавление метаданных
    Reflect.defineMetadata('column', options, target, propertyKey);
  };
};

// Использование
@Entity()
export class User {
  @Column({ type: 'varchar', length: 255 })
  email: string;
}
```

### Composition Decorators
```typescript
export const Auth = (...roles: Role[]) => {
  return applyDecorators(
    UseGuards(AuthGuard, RolesGuard),
    SetMetadata('roles', roles),
  );
};

// Использование
@Controller('admin')
@Auth(Role.ADMIN)
export class AdminController {}
```

### Method Decorator с биндингом
```typescript
export const Cache = (ttl: number = 60): MethodDecorator => {
  return (target, propertyKey, descriptor: PropertyDescriptor) => {
    const originalMethod = descriptor.value;
    
    descriptor.value = async function (...args: any[]) {
      const cacheKey = `${target.constructor.name}:${String(propertyKey)}`;
      // Кэширование логика
      return originalMethod.apply(this, args);
    };
    
    return descriptor;
  };
};

// Использование
@Cache(300)
@Get()
async findAll() {}
```

## Decorator Execution Order

```typescript
@Controller()
 ↓
@UseGuards()
 ↓
@UseInterceptors()
 ↓
@Get()
 ↓
method(@Param(), @Body())
```

## Best Practices

- **Single responsibility** — один декоратор = одна функция
- **Composition** — комбинируйте декораторы через applyDecorators
- **Type safety** — используйте generics для параметров
- **Naming** — имена в camelCase для параметров, PascalCase для классовых
- **Documentation** — документируйте custom decorators

## Смотрите также

- [GUARD.md](./GUARD.md) — @UseGuards и SetMetadata
- [PIPE.md](./PIPE.md) — @UsePipes и @Body/@Param
- [CONTROLLER.md](./CONTROLLER.md) — HTTP декораторы
- [NEST_JS_ARCHITECTURE.md](./NEST_JS_ARCHITECTURE.md) — Общая архитектура
