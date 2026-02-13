# Backend Testing

## Содержание

1. [TDD Подход](#tdd-подход)
2. [Unit Tests](#unit-tests)
3. [Integration Tests](#integration-tests)
4. [E2E Tests](#e2e-tests)
5. [Testing Cron Jobs](#testing-cron-jobs)
6. [Best Practices](#best-practices)

---

## TDD Подход

**Test-Driven Development:** сначала тест, потом код.

```
1. Написать failing test
2. Написать минимальный код для прохождения теста
3. Рефакторинг
4. Повторить
```

**Структура теста (AAA):**
```typescript
describe('UsersService', () => {
  describe('create', () => {
    it('should create user with valid data', async () => {
      // Arrange (Подготовка)
      const createUserDto = { email: 'test@test.com', password: 'password123' };
      
      // Act (Действие)
      const result = await service.create(createUserDto);
      
      // Assert (Проверка)
      expect(result).toHaveProperty('id');
      expect(result.email).toBe(createUserDto.email);
    });
  });
});
```

## Unit Tests

**Изоляция сервиса:**
```typescript
// users.service.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { UsersService } from './users.service';
import { UsersRepository } from './users.repository';

describe('UsersService', () => {
  let service: UsersService;
  let repository: jest.Mocked<UsersRepository>;

  beforeEach(async () => {
    const mockRepository = {
      findOne: jest.fn(),
      create: jest.fn(),
      save: jest.fn(),
    };

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UsersService,
        { provide: UsersRepository, useValue: mockRepository },
      ],
    }).compile();

    service = module.get<UsersService>(UsersService);
    repository = module.get(UsersRepository);
  });

  describe('findByEmail', () => {
    it('should return user if exists', async () => {
      const user = { id: '1', email: 'test@test.com' };
      repository.findOne.mockResolvedValue(user);

      const result = await service.findByEmail('test@test.com');

      expect(result).toEqual(user);
      expect(repository.findOne).toHaveBeenCalledWith({
        where: { email: 'test@test.com' },
      });
    });

    it('should return null if user not found', async () => {
      repository.findOne.mockResolvedValue(null);

      const result = await service.findByEmail('nonexistent@test.com');

      expect(result).toBeNull();
    });
  });
});
```

**Mocking dependencies:**
```typescript
// Мокаем внешние сервисы
const mockEmailService = {
  sendWelcomeEmail: jest.fn().mockResolvedValue(undefined),
};

// Проверяем вызовы
expect(mockEmailService.sendWelcomeEmail).toHaveBeenCalledWith(
  expect.objectContaining({ email: 'test@test.com' }),
);
```

## Integration Tests

**Тестирование модуля целиком:**
```typescript
// users.controller.spec.ts (integration)
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import request from 'supertest';

describe('UsersController (integration)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [
        TypeOrmModule.forRoot({
          type: 'sqlite',
          database: ':memory:',
          entities: [User],
          synchronize: true,
        }),
        UsersModule,
      ],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  describe('/users (POST)', () => {
    it('should create user', () => {
      return request(app.getHttpServer())
        .post('/users')
        .send({ email: 'test@test.com', password: 'password123' })
        .expect(201)
        .expect((res) => {
          expect(res.body).toHaveProperty('id');
          expect(res.body.email).toBe('test@test.com');
        });
    });

    it('should validate email format', () => {
      return request(app.getHttpServer())
        .post('/users')
        .send({ email: 'invalid-email', password: 'password123' })
        .expect(400);
    });
  });
});
```

**Тестовая база данных:**
```typescript
// test-database.module.ts
@Module({
  imports: [
    TypeOrmModule.forRootAsync({
      useFactory: () => ({
        type: 'better-sqlite3',
        database: ':memory:',
        entities: [__dirname + '/../**/*.entity{.ts,.js}'],
        synchronize: true,
        logging: false,
      }),
    }),
  ],
})
export class TestDatabaseModule {}
```

## E2E Tests

**Полный сценарий:**
```typescript
// test/app.e2e-spec.ts
describe('AppController (e2e)', () => {
  let app: INestApplication;
  let authToken: string;

  beforeAll(async () => {
    const moduleFixture = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();

    // Login to get token
    const response = await request(app.getHttpServer())
      .post('/auth/login')
      .send({ email: 'test@test.com', password: 'password' });
    
    authToken = response.body.access_token;
  });

  it('/profile (GET) - protected route', () => {
    return request(app.getHttpServer())
      .get('/profile')
      .set('Authorization', `Bearer ${authToken}`)
      .expect(200)
      .expect((res) => {
        expect(res.body.email).toBe('test@test.com');
      });
  });
});
```

## Testing Cron Jobs

**Unit тестирование:**
```typescript
// tasks.service.spec.ts
describe('TasksService', () => {
  let service: TasksService;
  let repository: jest.Mocked<ReportRepository>;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [
        TasksService,
        { provide: ReportRepository, useValue: mockRepository },
      ],
    }).compile();

    service = module.get<TasksService>(TasksService);
    repository = module.get(ReportRepository);
  });

  describe('generateDailyReport', () => {
    it('should generate report for yesterday', async () => {
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);

      await service.generateDailyReport();

      expect(repository.createDailyReport).toHaveBeenCalledWith(
        expect.objectContaining({
          date: expect.any(Date),
        }),
      );
    });

    it('should handle errors gracefully', async () => {
      repository.createDailyReport.mockRejectedValue(new Error('DB Error'));

      await expect(service.generateDailyReport()).rejects.toThrow('DB Error');
    });
  });
});
```

**Тестирование Schedule decorators:**
```typescript
// Проверка cron expression
import { SchedulerRegistry } from '@nestjs/schedule';

describe('Cron Job Registration', () => {
  it('should register daily report cron job', () => {
    const schedulerRegistry = app.get(SchedulerRegistry);
    const cronJobs = schedulerRegistry.getCronJobs();
    
    expect(cronJobs.has('daily-report')).toBe(true);
  });
});
```

## Best Practices

**Coverage:**
```json
// jest.config.js
{
  "coverageThreshold": {
    "global": {
      "branches": 80,
      "functions": 80,
      "lines": 80,
      "statements": 80
    }
  }
}
```

**Изоляция тестов:**
```typescript
// ✅ Каждый тест независим
beforeEach(async () => {
  await repository.clear(); // Очищаем перед каждым тестом
});

// ✅ Не используем общий state между тестами
// ❌ Не делайте так:
let sharedUser: User;
beforeAll(async () => {
  sharedUser = await createUser(); // Проблемы при параллельном запуске
});
```

**Нейминг:**
```typescript
// ✅ Понятные описания
describe('when user already exists', () => {
  it('should throw ConflictException', async () => {
    // ...
  });
});

// ✅ Given-When-Then
describe('Given a valid user', () => {
  describe('When creating user', () => {
    it('Then should return created user', async () => {
      // ...
    });
  });
});
```

**Factory pattern для тестовых данных:**
```typescript
// test/factories/user.factory.ts
export const createUserDto = (overrides = {}) => ({
  email: faker.internet.email(),
  password: faker.internet.password(),
  name: faker.person.fullName(),
  ...overrides,
});

// Использование
const dto = createUserDto({ email: 'specific@test.com' });
```
