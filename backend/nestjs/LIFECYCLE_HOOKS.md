# Lifecycle Hooks

## Содержание

1. [Что такое Lifecycle Hooks](#что-такое-lifecycle-hooks)
2. [Назначение](#назначение)
3. [Базовый синтаксис](#базовый-синтаксис)
4. [Практические примеры](#практические-примеры)
5. [Best Practices](#best-practices)
6. [Смотрите также](#смотрите-также)

---

## Что такое Lifecycle Hooks

Lifecycle Hooks — интерфейсы, позволяющие выполнять код на определённых этапах жизни модуля или приложения. Позволяют инициализировать ресурсы при старте и корректно освобождать при завершении.

## Назначение

- **Initialization** — настройка при старте модуля
- **Connection setup** — подключение к БД, Redis, внешним API
- **Warmup** — предварительная загрузка кэша
- **Cleanup** — закрытие соединений при завершении
- **Graceful shutdown** — корректное завершение работы

## Базовый синтаксис

```typescript
@Injectable()
export class DatabaseService implements OnModuleInit, OnApplicationShutdown {
  async onModuleInit() {
    // Инициализация при старте модуля
  }

  async onApplicationShutdown(signal?: string) {
    // Очистка при завершении приложения
  }
}
```

## Практические примеры

### OnModuleInit
```typescript
@Injectable()
export class CacheService implements OnModuleInit {
  private cache = new Map<string, any>();

  async onModuleInit() {
    // Предварительная загрузка данных
    const configs = await this.configRepository.find();
    configs.forEach(config => {
      this.cache.set(config.key, config.value);
    });
    console.log('Cache initialized');
  }
}
```

### OnApplicationBootstrap
```typescript
@Injectable()
export class NotificationService implements OnApplicationBootstrap {
  async onApplicationBootstrap() {
    // Сервис полностью инициализирован, можно использовать другие сервисы
    await this.connectToWebSocket();
    console.log('WebSocket connected');
  }
}
```

### OnModuleDestroy
```typescript
@Injectable()
export class DatabaseConnection implements OnModuleDestroy {
  private connection: Connection;

  async onModuleDestroy() {
    if (this.connection?.isConnected) {
      await this.connection.close();
      console.log('Database connection closed');
    }
  }
}
```

### OnApplicationShutdown
```typescript
@Injectable()
export class RedisService implements OnApplicationShutdown {
  private client: RedisClient;

  async onApplicationShutdown(signal: string) {
    console.log(`Received shutdown signal: ${signal}`);
    
    if (this.client?.isReady) {
      await this.client.quit();
      console.log('Redis connection closed gracefully');
    }
  }
}
```

### BeforeApplicationShutdown
```typescript
@Injectable()
export class QueueService implements BeforeApplicationShutdown {
  private isShuttingDown = false;

  async beforeApplicationShutdown(signal: string) {
    this.isShuttingDown = true;
    
    // Дождаться завершения текущих задач
    while (this.activeJobs > 0) {
      await sleep(1000);
    }
    
    console.log('All jobs completed, ready for shutdown');
  }
}
```

### Module-level hooks
```typescript
@Module({})
export class DatabaseModule implements OnModuleInit {
  constructor(private configService: ConfigService) {}

  async onModuleInit() {
    const dbConfig = this.configService.get('database');
    await this.initializeConnection(dbConfig);
  }
}
```

## Execution Order

```
Application Start:
  1. OnModuleInit (для каждого модуля)
  2. OnApplicationBootstrap (для каждого модуля)

Application Shutdown:
  1. beforeApplicationShutdown (опционально)
  2. onModuleDestroy
  3. onApplicationShutdown
```

## Enable Shutdown Hooks

```typescript
// main.ts
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  // Включаем graceful shutdown
  app.enableShutdownHooks();
  
  await app.listen(3000);
}
```

## Best Practices

- **Async/await** — используйте для асинхронных операций
- **Error handling** — обрабатывайте ошибки инициализации
- **Timeout** — добавляйте таймауты для внешних подключений
- **Graceful degradation** — не падать, если необязательный сервис недоступен
- **Idempotency** — hooks должны быть безопасны для повторного вызова
- **Logging** — логируйте этапы инициализации и завершения

## Смотрите также

- [MODULE.md](./MODULE.md) — Регистрация провайдеров
- [SERVICE.md](./SERVICE.md) — Создание сервисов
- [NEST_JS_ARCHITECTURE.md](./NEST_JS_ARCHITECTURE.md) — Общая архитектура
