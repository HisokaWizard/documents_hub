# Entity

## Содержание

1. [Что такое Entity](#что-такое-entity)
2. [Назначение](#назначение)
3. [Базовый синтаксис](#базовый-синтаксис)
4. [Практические примеры](#практические-примеры)
5. [Best Practices](#best-practices)
6. [Смотрите также](#смотрите-также)

---

## Что такое Entity

Entity — класс, представляющий таблицу в базе данных. Определяет структуру данных, типы полей и связи между таблицами с помощью TypeORM декораторов.

## Назначение

- **Schema definition** — определение структуры таблиц БД
- **Type safety** — типизация данных на уровне TypeScript
- **ORM mapping** — маппинг объектов на реляционные таблицы
- **Relations** — определение связей между сущностями
- **Validation** — constraints на уровне БД

## Базовый синтаксис

```typescript
@Entity('users')
export class User {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ type: 'varchar', length: 255, unique: true })
  email: string;

  @Column({ type: 'varchar', length: 255 })
  password: string;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
```

## Практические примеры

### Базовая сущность
```typescript
@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  firstName: string;

  @Column()
  lastName: string;

  @Column({ default: true })
  isActive: boolean;
}
```

### Relations
```typescript
@Entity()
export class User {
  @OneToOne(() => Profile, profile => profile.user)
  @JoinColumn()
  profile: Profile;

  @OneToMany(() => Post, post => post.author)
  posts: Post[];

  @ManyToMany(() => Role, role => role.users)
  @JoinTable()
  roles: Role[];
}

@Entity()
export class Post {
  @ManyToOne(() => User, user => user.posts)
  author: User;
}
```

### Column types и options
```typescript
@Entity()
export class Product {
  @Column('decimal', { precision: 10, scale: 2 })
  price: number;

  @Column('text', { nullable: true })
  description: string;

  @Column('jsonb', { default: {} })
  metadata: Record<string, any>;

  @Column('enum', { enum: Status, default: Status.DRAFT })
  status: Status;
}
```

### Indexes
```typescript
@Entity()
@Index(['email', 'status'])
@Index(['createdAt'])
export class User {
  @Column({ unique: true })
  email: string;

  @Index()
  @Column()
  status: string;
}
```

### Lifecycle callbacks
```typescript
@Entity()
export class User {
  @BeforeInsert()
  hashPassword() {
    this.password = bcrypt.hashSync(this.password, 10);
  }

  @BeforeUpdate()
  updateTimestamp() {
    this.updatedAt = new Date();
  }
}
```

## Best Practices

- **Naming** — сущности в PascalCase (User, Order, Product)
- **Relations** — определяйте bidirectional связи аккуратно
- **Indexes** — добавляйте для часто используемых полей
- **Constraints** — используйте unique, nullable, default
- **Soft delete** — рассмотрите @DeleteDateColumn вместо hard delete
- **DTO separation** — не используйте Entity как DTO

## Смотрите также

- [REPOSITORY.md](./REPOSITORY.md) — Работа с сущностями
- [SERVICE.md](./SERVICE.md) — Бизнес-логика
- [NEST_JS_ARCHITECTURE.md](./NEST_JS_ARCHITECTURE.md) — Общая архитектура
