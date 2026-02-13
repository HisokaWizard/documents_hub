# TypeScript

## Содержание

1. [Конфигурация](#конфигурация)
2. [Типизация Props](#типизация-props)
3. [Generics](#generics)
4. [Utility Types](#utility-types)
5. [Best Practices](#best-practices)

---

## Конфигурация

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  }
}
```

## Типизация Props

```tsx
// Interface для объектов
interface UserProps {
  id: string;
  name: string;
  email: string;
  isActive?: boolean;
}

// Type для unions
type Status = 'idle' | 'loading' | 'success' | 'error';

// Component props
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({ variant = 'primary', isLoading, children, ...props }) => {
  return <button {...props}>{isLoading ? <Spinner /> : children}</button>;
};
```

## Generics

```tsx
// Generic hook
function useApi<T>(url: string): { data: T | null; loading: boolean } {
  const [data, setData] = useState<T | null>(null);
  // ... implementation
  return { data, loading };
}

// Generic component
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

export function List<T>({ items, renderItem }: ListProps<T>) {
  return <ul>{items.map(renderItem)}</ul>;
}

// Usage
<List<User> items={users} renderItem={user => <UserCard user={user} />} />
```

## Utility Types

```tsx
// Pick/Omit
type UserPreview = Pick<User, 'id' | 'name'>;
type CreateUserDto = Omit<User, 'id' | 'createdAt'>;

// Partial/Required
type PartialUser = Partial<User>;
type RequiredUser = Required<User>;

// Record
const config: Record<string, string> = { apiUrl: 'http://localhost' };

// ReturnType
type FetchUsersReturn = ReturnType<typeof fetchUsers>;

// Parameters
type FetchUsersParams = Parameters<typeof fetchUsers>;
```

## Best Practices

```tsx
// Strict null checks
const [user, setUser] = useState<User | null>(null);
if (!user) return null; // Type guard

// Discriminated unions
interface LoadingState { status: 'loading'; }
interface SuccessState { status: 'success'; data: User; }
interface ErrorState { status: 'error'; error: Error; }
type State = LoadingState | SuccessState | ErrorState;

// Exhaustive checks
function handleState(state: State) {
  switch (state.status) {
    case 'loading': return <Spinner />;
    case 'success': return <UserCard user={state.data} />;
    case 'error': return <Error message={state.error.message} />;
    default: const _exhaustive: never = state;
  }
}

// Type inference
const user = { name: 'John', age: 30 }; // TypeScript infer type
const users: typeof user[] = []; // Reuse inferred type
```

## Strict Mode Рекомендации

- Всегда включен strict mode
- Явное указание return types для public API
- Избегать `any` — использовать `unknown` с type guards
- No implicit any в function parameters
