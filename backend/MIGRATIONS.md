# Database Migrations

## Содержание

1. [Что такое миграции](#что-такое-миграции)
2. [TypeORM Migrations](#typeorm-migrations)
3. [Структура миграции](#структура-миграции)
4. [CLI команды](#cli-команды)
5. [Best Practices](#best-practices)
6. [Seeding](#seeding)

---

## Что такое миграции

Миграции — версионирование схемы базы данных. Позволяют отслеживать изменения структуры БД, применять их к разным окружениям и откатывать при необходимости.

**Зачем нужны:**
- Версионирование структуры БД в Git
- Совместная работа команды
- Деплой на production
- Rollback при ошибках
- Консистентность окружений (dev, staging, prod)

## TypeORM Migrations

**Конфигурация:**
```typescript
// typeorm.config.ts
import { DataSource } from 'typeorm';

export const AppDataSource = new DataSource({
  type: 'postgres',
  host: 'localhost',
  port: 5432,
  username: 'user',
  password: 'password',
  database: 'mydb',
  entities: ['dist/**/*.entity.js'],
  migrations: ['dist/database/migrations/*.js'],
  synchronize: false, // В production всегда false!
});
```

**package.json:**
```json
{
  "scripts": {
    "migration:generate": "typeorm-ts-node-commonjs migration:generate",
    "migration:create": "typeorm-ts-node-commonjs migration:create",
    "migration:run": "typeorm-ts-node-commonjs migration:run",
    "migration:revert": "typeorm-ts-node-commonjs migration:revert"
  }
}
```

## Структура миграции

```typescript
// database/migrations/1699999999999-CreateUsersTable.ts
import { MigrationInterface, QueryRunner, Table } from 'typeorm';

export class CreateUsersTable1699999999999 implements MigrationInterface {
  name = 'CreateUsersTable1699999999999';

  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.createTable(
      new Table({
        name: 'users',
        columns: [
          {
            name: 'id',
            type: 'uuid',
            isPrimary: true,
            generationStrategy: 'uuid',
            default: 'uuid_generate_v4()',
          },
          {
            name: 'email',
            type: 'varchar',
            length: '255',
            isUnique: true,
          },
          {
            name: 'password',
            type: 'varchar',
            length: '255',
          },
          {
            name: 'created_at',
            type: 'timestamp',
            default: 'CURRENT_TIMESTAMP',
          },
        ],
      }),
      true,
    );
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.dropTable('users');
  }
}
```

**Добавление колонки:**
```typescript
// database/migrations/1700000000000-AddUserStatus.ts
import { MigrationInterface, QueryRunner, TableColumn } from 'typeorm';

export class AddUserStatus1700000000000 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.addColumn(
      'users',
      new TableColumn({
        name: 'status',
        type: 'enum',
        enum: ['active', 'inactive', 'banned'],
        default: `'active'`,
      }),
    );
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.dropColumn('users', 'status');
  }
}
```

**Создание связей:**
```typescript
// Добавление foreign key
public async up(queryRunner: QueryRunner): Promise<void> {
  await queryRunner.createForeignKey(
    'posts',
    new TableForeignKey({
      columnNames: ['user_id'],
      referencedColumnNames: ['id'],
      referencedTableName: 'users',
      onDelete: 'CASCADE',
    }),
  );
}
```

## CLI команды

```bash
# Автоматическая генерация миграции по изменениям в entities
npm run migration:generate -- src/database/migrations/AddUserProfile

# Создание пустой миграции
npm run migration:create -- src/database/migrations/ManualDataFix

# Применение миграций
npm run migration:run

# Откат последней миграции
npm run migration:revert

# Просмотр статуса
npx typeorm-ts-node-commonjs migration:show
```

## Best Practices

**Нейминг:**
```
YYYYMMDDHHMMSS-DescriptiveName.ts
1700000000000-CreateUsersTable.ts
1700000000001-AddPostsTable.ts
1700000000002-AddUserStatusColumn.ts
```

**Атомарность:**
```typescript
// ✅ Одна миграция = одна логическая операция
// ❌ Не смешивайте создание таблиц и изменение данных

// ✅ Обработка существующих данных при добавлении NOT NULL
public async up(queryRunner: QueryRunner): Promise<void> {
  // 1. Добавляем nullable колонку
  await queryRunner.addColumn('users', new TableColumn({
    name: 'phone',
    type: 'varchar',
    isNullable: true,
  }));
  
  // 2. Заполняем дефолтными значениями
  await queryRunner.query(`UPDATE users SET phone = 'unknown'`);
  
  // 3. Делаем NOT NULL
  await queryRunner.changeColumn('users', 'phone', new TableColumn({
    name: 'phone',
    type: 'varchar',
    isNullable: false,
  }));
}
```

**Никогда не изменяйте применённые миграции!** Создавайте новые.

**Идемпотентность:**
```typescript
// ✅ Проверка существования перед созданием
public async up(queryRunner: QueryRunner): Promise<void> {
  const tableExists = await queryRunner.hasTable('users');
  if (!tableExists) {
    await queryRunner.createTable(/* ... */);
  }
}
```

## Seeding

Наполнение БД тестовыми данными.

```typescript
// database/seeds/user.seed.ts
import { DataSource } from 'typeorm';
import { Seeder } from 'typeorm-extension';
import { User } from '../../src/modules/users/entities/user.entity';

export default class UserSeeder implements Seeder {
  public async run(dataSource: DataSource): Promise<void> {
    const repository = dataSource.getRepository(User);
    
    await repository.insert([
      { email: 'admin@example.com', name: 'Admin' },
      { email: 'user@example.com', name: 'User' },
    ]);
  }
}

// package.json
{
  "scripts": {
    "seed": "ts-node -r tsconfig-paths/register ./node_modules/typeorm-extension/bin/cli.cjs seed:run"
  }
}
```

**Сиды для тестов:**
```typescript
// test/utils/test-database.ts
export async function setupTestDatabase() {
  const dataSource = await AppDataSource.initialize();
  await dataSource.runMigrations();
  
  // Seed test data
  const userRepo = dataSource.getRepository(User);
  await userRepo.save({ email: 'test@test.com', name: 'Test User' });
  
  return dataSource;
}

export async function teardownTestDatabase(dataSource: DataSource) {
  await dataSource.dropDatabase();
  await dataSource.destroy();
}
```
