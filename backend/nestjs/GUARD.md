# Guard

## Содержание

1. [Что такое Guard](#что-такое-guard)
2. [Назначение](#назначение)
3. [Базовый синтаксис](#базовый-синтаксис)
4. [Практические примеры](#практические-примеры)
5. [Best Practices](#best-practices)
6. [Смотрите также](#смотрите-также)

---

## Что такое Guard

Guard — компонент, определяющий, может ли текущий пользователь выполнить запрос. Реализует авторизацию и аутентификацию на уровне маршрутов или всего приложения.

## Назначение

- **Authentication** — проверка, что пользователь авторизован
- **Authorization** — проверка прав доступа
- **Role-based access** — доступ по ролям
- **Permission-based access** — доступ по разрешениям
- **Route protection** — защита эндпоинтов

## Базовый синтаксис

```typescript
@Injectable()
export class AuthGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean | Promise<boolean> | Observable<boolean> {
    const request = context.switchToHttp().getRequest();
    return validateRequest(request);
  }
}

@Controller('users')
@UseGuards(AuthGuard)
export class UsersController {}
```

## Практические примеры

### JWT Guard
```typescript
@Injectable()
export class JwtAuthGuard implements CanActivate {
  constructor(private jwtService: JwtService) {}

  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const token = this.extractTokenFromHeader(request);
    
    if (!token) {
      throw new UnauthorizedException();
    }
    
    try {
      const payload = this.jwtService.verify(token);
      request.user = payload;
      return true;
    } catch {
      throw new UnauthorizedException();
    }
  }

  private extractTokenFromHeader(request: Request): string | undefined {
    const [type, token] = request.headers.authorization?.split(' ') ?? [];
    return type === 'Bearer' ? token : undefined;
  }
}
```

### Roles Guard
```typescript
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<Role[]>('roles', [
      context.getHandler(),
      context.getClass(),
    ]);
    
    if (!requiredRoles) {
      return true;
    }
    
    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.some(role => user.roles?.includes(role));
  }
}

// Декоратор
export const Roles = (...roles: Role[]) => SetMetadata('roles', roles);

// Использование
@Controller('admin')
@Roles(Role.ADMIN)
@UseGuards(RolesGuard)
export class AdminController {}
```

### Permission Guard
```typescript
@Injectable()
export class PermissionsGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredPermissions = this.reflector.get<string[]>('permissions', context.getHandler());
    const request = context.switchToHttp().getRequest();
    const user = request.user;
    
    return requiredPermissions.every(permission => user.permissions.includes(permission));
  }
}
```

### Composite Guard
```typescript
@Injectable()
export class AuthRolesGuard implements CanActivate {
  constructor(
    private jwtGuard: JwtAuthGuard,
    private rolesGuard: RolesGuard,
  ) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const jwtResult = await this.jwtGuard.canActivate(context);
    if (!jwtResult) return false;
    
    return this.rolesGuard.canActivate(context);
  }
}
```

### Global Guard
```typescript
// В main.ts
app.useGlobalGuards(new JwtAuthGuard(jwtService));

// Или в модуле
providers: [
  {
    provide: APP_GUARD,
    useClass: JwtAuthGuard,
  },
]
```

## Best Practices

- **Early return** — проверяйте самые быстрые условия первыми
- **Throw exceptions** — выбрасывайте специфические ошибки (Unauthorized, Forbidden)
- **Metadata** — используйте Reflector для декларативной авторизации
- **Composition** — комбинируйте guards через @UseGuards(Guard1, Guard2)
- **Global guards** — регистрируйте JWT guard глобально

## Смотрите также

- [MIDDLEWARE.md](./MIDDLEWARE.md) — Middleware для аутентификации
- [CONTROLLER.md](./CONTROLLER.md) — Применение guards
- [DECORATOR.md](./DECORATOR.md) — Создание @Roles декоратора
- [NEST_JS_ARCHITECTURE.md](./NEST_JS_ARCHITECTURE.md) — Общая архитектура
