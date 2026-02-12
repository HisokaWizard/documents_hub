# Repository

## Содержание

1. [Что такое Repository](#что-такое-repository)
2. [Назначение](#назначение)
3. [Базовый синтаксис](#базовый-синтаксис)
4. [Практические примеры](#практические-примеры)
5. [Best Practices](#best-practices)
6. [Смотрите также](#смотрите-также)

---

## Что такое Repository

Repository — паттерн проектирования, абстрагирующий логику доступа к данным. Инкапсулирует CRUD операции и сложные запросы к базе данных.

## Назначение

- **Abstraction** — скрытие деталей работы с БД
- **Reusability** — централизация запросов
- **Testability** — легкое мокирование доступа к данным
- **Separation of concerns** — отделение бизнес-логики от persistence
- **Flexibility** — возможность смены ORM без изменения сервисов

## Базовый синтаксис

```typescript
@Injectable()
export class UsersRepository {
  constructor(@InjectRepository(User) private repository: Repository<User>) {}

  async findAll(): Promise<User[]> {
    return this.repository.find();
  }

  async findOne(id: string): Promise<User | null> {
    return this.repository.findOne({ where: { id } });
  }

  async create(user: Partial<User>): Promise<User> {
    const entity = this.repository.create(user);
    return this.repository.save(entity);
  }
}
```

## Практические примеры

### TypeORM Repository
```typescript
@Injectable()
export class UsersRepository extends Repository<User> {
  constructor(private dataSource: DataSource) {
    super(User, dataSource.createEntityManager());
  }

  async findByEmail(email: string): Promise<User | null> {
    return this.findOne({ where: { email } });
  }
}
```

### Custom repository с QueryBuilder
```typescript
@Injectable()
export class UsersRepository {
  async findWithPosts(userId: string): Promise<User> {
    return this.repository
      .createQueryBuilder('user')
      .leftJoinAndSelect('user.posts', 'posts')
      .where('user.id = :id', { id: userId })
      .getOne();
  }
}
```

### Prisma Repository
```typescript
@Injectable()
export class UsersRepository {
  constructor(private prisma: PrismaService) {}

  async findAll(): Promise<User[]> {
    return this.prisma.user.findMany();
  }

  async create(data: Prisma.UserCreateInput): Promise<User> {
    return this.prisma.user.create({ data });
  }
}
```

### Repository с транзакциями
```typescript
@Injectable()
export class OrderRepository {
  async createOrderWithItems(orderData: CreateOrderDto, items: OrderItem[]) {
    return this.dataSource.transaction(async manager => {
      const order = await manager.save(Order, orderData);
      await manager.save(OrderItem, items.map(item => ({ ...item, orderId: order.id })));
      return order;
    });
  }
}
```

### Repository с пагинацией
```typescript
@Injectable()
export class UsersRepository {
  async findPaginated(page: number, limit: number): Promise<[User[], number]> {
    return this.repository.findAndCount({
      skip: (page - 1) * limit,
      take: limit,
    });
  }
}
```

## Best Practices

- **One repository per entity** — репозиторий для каждой сущности
- **No business logic** — только CRUD и запросы
- **Return entities** — возвращайте сущности, не raw SQL
- **Handle nulls** — обрабатывайте случаи, когда данные не найдены
- **Use QueryBuilder** — для сложных запросов вместо raw SQL

## Смотрите также

- [ENTITY.md](./ENTITY.md) — Определение сущностей
- [SERVICE.md](./SERVICE.md) — Использование репозиториев
- [DEPENDENCY_INJECTION.md](./DEPENDENCY_INJECTION.md) — Внедрение репозиториев
- [NEST_JS_ARCHITECTURE.md](./NEST_JS_ARCHITECTURE.md) — Общая архитектура
