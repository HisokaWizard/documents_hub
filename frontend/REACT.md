# React

## Содержание

1. [Версия и требования](#версия-и-требования)
2. [Functional Components](#functional-components)
3. [Основные Hooks](#основные-hooks)
4. [Паттерны](#паттерны)
5. [Best Practices](#best-practices)

---

## Версия и требования

**React 18+**
- Concurrent Features
- Automatic Batching
- Transitions API
- Suspense improvements
- Strict Mode enabled

## Functional Components

```tsx
// Базовый компонент
interface UserCardProps {
  user: User;
  onEdit: (id: string) => void;
}

export const UserCard: React.FC<UserCardProps> = ({ user, onEdit }) => {
  return (
    <Card>
      <Typography>{user.name}</Typography>
      <Button onClick={() => onEdit(user.id)}>Edit</Button>
    </Card>
  );
};

// Memoized компонент
export const ExpensiveList = React.memo<ListProps>(({ items }) => {
  return <ul>{items.map(renderItem)}</ul>;
});
```

## Основные Hooks

```tsx
// useState
const [count, setCount] = useState<number>(0);

// useEffect
useEffect(() => {
  fetchData();
  return () => cleanup();
}, [dependency]);

// useCallback
const handleClick = useCallback(() => {
  console.log('clicked');
}, []);

// useMemo
const sortedData = useMemo(() => {
  return data.sort((a, b) => a.value - b.value);
}, [data]);

// useRef
const inputRef = useRef<HTMLInputElement>(null);

// Custom hook
const useToggle = (initial = false) => {
  const [state, setState] = useState(initial);
  const toggle = useCallback(() => setState(s => !s), []);
  return [state, toggle] as const;
};
```

## Паттерны

**Container/Presentational**
```tsx
// Container - logic
export const UserListContainer = () => {
  const { data, isLoading } = useGetUsersQuery();
  return <UserList users={data} loading={isLoading} />;
};

// Presentational - UI
export const UserList: React.FC<UserListProps> = ({ users, loading }) => {
  if (loading) return <Spinner />;
  return <List>{users.map(user => <UserCard key={user.id} user={user} />)}</List>;
};
```

**Compound Components**
```tsx
// Tabs.tsx
export const Tabs = ({ children }: { children: React.ReactNode }) => {
  const [activeTab, setActiveTab] = useState(0);
  return <TabsContext.Provider value={{ activeTab, setActiveTab }}>{children}</TabsContext.Provider>;
};

Tabs.List = TabsList;
Tabs.Tab = Tab;
Tabs.Panel = TabPanel;
```

**Render Props**
```tsx
<DataFetcher url="/api/users">
  {({ data, loading }) => loading ? <Spinner /> : <List data={data} />}
</DataFetcher>
```

## Best Practices

- **Ключи** — всегда stable keys, не используйте index при сортировке
- **Memoization** — useMemo/useCallback только для дорогих вычислений
- **Cleanup** — очищайте подписки и таймеры в useEffect
- **Lazy loading** — React.lazy + Suspense для code splitting
- **Error Boundaries** — оборачивайте критические части приложения
