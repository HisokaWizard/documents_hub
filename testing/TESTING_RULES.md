# Testing Rules

## Содержание

1. [TDD: Red-Green-Refactor](#tdd-red-green-refactor)
2. [Цикл разработки](#цикл-разработки)
3. [Частные правила тестирования](#частные-правила-тестирования)

---

## TDD: Red-Green-Refactor

Test-Driven Development (TDD) — методология разработки, при которой тесты пишутся **до** написания production-кода.

### Цикл Red-Green-Refactor

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│  RED    │ ──▶ │ GREEN   │ ──▶ │ REFACTOR│
│  Fail   │     │  Pass   │     │ Improve │
└─────────┘     └─────────┘     └─────────┘
     ▲                                │
     └────────────────────────────────┘
```

### Шаги цикла

#### 1. RED — Написать падающий тест

Сначала пишем тест, который **обязательно падает**.

```typescript
// users.service.spec.ts
// Шаг 1: Пишем тест ДО реализации

describe('UsersService', () => {
  describe('create', () => {
    it('should create user with valid data', async () => {
      // Arrange
      const createUserDto = {
        email: 'test@test.com',
        password: 'password123',
      };

      // Act
      const result = await service.create(createUserDto);

      // Assert
      expect(result).toHaveProperty('id');
      expect(result.email).toBe(createUserDto.email);
    });
  });
});
```

**Принципы:**

- Тест описывает желаемое поведение
- Тест компилируется, но падает при выполнении
- Падает по правильной причине (не из-за ошибки в тесте)
- Думайте о том, КАК должен работать код

#### 2. GREEN — Минимальный код для прохождения

Пишем **минимально необходимый** код, чтобы тест прошел.

```typescript
// users.service.ts
// Шаг 2: Минимальная реализация

@Injectable()
export class UsersService {
  async create(createUserDto: CreateUserDto): Promise<User> {
    // Самый простой код для прохождения теста
    return {
      id: 'uuid-generated',
      email: createUserDto.email,
      password: 'hashed',
    } as User;
  }
}
```

**Принципы:**

- Делайте проще, чем нужно
- Дублируйте код, если нужно
- Используйте жестко закодированные значения
- Главное — зеленый тест

#### 3. REFACTOR — Улучшение кода

Улучшаем код, сохраняя зеленые тесты.

```typescript
// users.service.ts
// Шаг 3: Рефакторинг с сохранением поведения

@Injectable()
export class UsersService {
  constructor(
    private readonly usersRepository: UsersRepository,
    private readonly passwordService: PasswordService,
  ) {}

  async create(createUserDto: CreateUserDto): Promise<User> {
    // Проверяем уникальность email
    const existing = await this.usersRepository.findByEmail(createUserDto.email);
    if (existing) {
      throw new ConflictException('Email already exists');
    }

    // Хешируем пароль
    const hashedPassword = await this.passwordService.hash(createUserDto.password);

    // Создаем пользователя
    const user = this.usersRepository.create({
      ...createUserDto,
      password: hashedPassword,
    });

    return this.usersRepository.save(user);
  }
}
```

**Принципы:**

- Удаляйте дублирование
- Улучшайте читаемость
- Добавляйте обработку ошибок
- Не меняйте поведение — тесты должны оставаться зелеными

---

## Цикл разработки

### Полный цикл для новой фичи

```
1. Выбрать маленький кусок функциональности
2. Написать падающий тест (RED)
3. Запустить тест — убедиться, что он падает
4. Написать минимальный код (GREEN)
5. Запустить тест — убедиться, что проходит
6. Рефакторить код (REFACTOR)
7. Запустить все тесты — ничего не сломалось
8. Повторить с шага 1
```

### Пример полного цикла

```typescript
// Итерация 1: Базовая функциональность
describe('Calculator', () => {
  it('should add two numbers', () => {
    expect(calculator.add(2, 3)).toBe(5);  // RED
  });
});

// Минимальная реализация
add(a: number, b: number): number {
  return 5;  // GREEN (hardcoded)
}

// Итерация 2: Универсальность
describe('Calculator', () => {
  it('should add two numbers', () => {
    expect(calculator.add(2, 3)).toBe(5);
  });

  it('should add different numbers', () => {
    expect(calculator.add(10, 20)).toBe(30);  // RED
  });
});

// Улучшенная реализация
add(a: number, b: number): number {
  return a + b;  // GREEN (универсально)
}

// Итерация 3: Обработка граничных случаев
describe('Calculator', () => {
  it('should handle negative numbers', () => {
    expect(calculator.add(-5, 3)).toBe(-2);  // RED
  });
});

// Рефакторинг и доработка
add(a: number, b: number): number {
  if (typeof a !== 'number' || typeof b !== 'number') {
    throw new Error('Invalid arguments');
  }
  return a + b;  // GREEN + REFACTOR
}
```

---

## Структура теста (AAA)

```typescript
describe('Feature', () => {
  it('should behave correctly', async () => {
    // Arrange — Подготовка
    const input = { email: 'test@test.com' };
    const expectedOutput = { id: '1', email: 'test@test.com' };

    // Act — Действие
    const result = await service.create(input);

    // Assert — Проверка
    expect(result).toEqual(expectedOutput);
  });
});
```

---

## Частные правила тестирования - ОБЯЗАТЕЛЬНО к прочтению

**Данные правила строго необходимо прочитать для валидного написания тестов по направлениям**s

Для детальных правил тестирования в конкретных областях обратитесь к:

### Frontend Testing

**Файл:** [`./frontend/TESTING.md`](../frontend/TESTING.md)

Содержит правила для:

- Unit testing React компонентов
- Testing Library best practices
- E2E тестирование с Playwright
- Тестирование hooks и Redux

### Backend Testing

**Файл:** [`./backend/BACKEND_TESTING.md`](../backend/BACKEND_TESTING.md)

Содержит правила для:

- Unit тестирование NestJS сервисов
- Integration тестирование контроллеров
- Тестирование с in-memory базой данных
- Тестирование cron jobs
- Coverage thresholds

---

## Golden Rules

1. **Тесты первыми** — всегда пишите тест до кода
2. **Один тест — одна концепция** — не тестируйте все сразу
3. **Тесты как документация** — описывайте поведение, а не реализацию
4. **Быстрые тесты** — unit тесты должны выполняться за миллисекунды
5. **Независимые тесты** — порядок выполнения не должен влиять
6. **Детерминированные** — один и тот же результат при каждом запуске

```typescript
// ✅ Хорошо: Тест описывает поведение
it('should send welcome email after registration', () => {
  // ...
});

// ❌ Плохо: Тест описывает реализацию
it('should call emailService.sendWelcomeEmail with correct params', () => {
  // ...
});
```
