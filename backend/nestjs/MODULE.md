# Module

## Содержание

1. [Что такое Module](#что-такое-module)
2. [Назначение](#назначение)
3. [Базовый синтаксис](#базовый-синтаксис)
4. [Практические примеры](#практические-примеры)
5. [Best Practices](#best-practices)
6. [Смотрите также](#смотрите-также)

---

## Что такое Module

Module в NestJS — это организационная единица, группирующая связанные компоненты приложения: контроллеры, провайдеры, модули и экспорты. `@Module()` декоратор определяет метаданные модуля.

## Назначение

- **Инкапсуляция** — группировка связанной функциональности
- **Организация** — структурирование приложения по доменам
- **Reusability** — переиспользование модулей между проектами
- **Dependency management** — управление зависимостями между модулями

## Базовый синтаксис

```typescript
@Module({
  imports: [],      // Импортируемые модули
  controllers: [],  // Контроллеры модуля
  providers: [],    // Сервисы и провайдеры
  exports: []       // Экспортируемые провайдеры
})
export class UsersModule {}
```

## Практические примеры

### Корневой модуль
```typescript
@Module({
  imports: [UsersModule, AuthModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
```

### Feature модуль
```typescript
@Module({
  imports: [TypeOrmModule.forFeature([User])],
  controllers: [UsersController],
  providers: [UsersService, UsersRepository],
  exports: [UsersService]
})
export class UsersModule {}
```

### Глобальный модуль
```typescript
@Global()
@Module({
  providers: [ConfigService],
  exports: [ConfigService]
})
export class ConfigModule {}
```

### Динамический модуль
```typescript
@Module({})
export class DatabaseModule {
  static forRoot(options: Config): DynamicModule {
    return {
      module: DatabaseModule,
      providers: [{ provide: 'CONFIG', useValue: options }],
      exports: ['CONFIG']
    };
  }
}
```

## Best Practices

- **Single Responsibility** — один модуль = один домен
- **Feature-based** — организация по функциональности, не по типу
- **Shared модуль** — выносите переиспользуемое в SharedModule
- **Avoid циклических зависимостей** — используйте forwardRef() при необходимости

## Смотрите также

- [CONTROLLER.md](./CONTROLLER.md) — HTTP обработка
- [SERVICE.md](./SERVICE.md) — Бизнес-логика
- [DEPENDENCY_INJECTION.md](./DEPENDENCY_INJECTION.md) — Внедрение зависимостей
- [NEST_JS_ARCHITECTURE.md](./NEST_JS_ARCHITECTURE.md) — Общая архитектура
