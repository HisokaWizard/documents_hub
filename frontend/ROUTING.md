# Routing

## Содержание

1. [Базовая конфигурация](#базовая-конфигурация)
2. [Nested Routes](#nested-routes)
3. [Data Loaders](#data-loaders)
4. [Programmatic Navigation](#programmatic-navigation)
5. [Protected Routes](#protected-routes)

---

## Базовая конфигурация

```tsx
// router/index.tsx
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { RootLayout } from '@/app/layouts/RootLayout';
import { HomePage } from '@/pages/home';
import { ProfilePage } from '@/pages/profile';
import { LoginPage } from '@/pages/login';
import { NotFoundPage } from '@/pages/not-found';

const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'profile', element: <ProfilePage /> },
      { path: 'login', element: <LoginPage /> },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
]);

// App.tsx
export const App = () => <RouterProvider router={router} />;
```

## Nested Routes

```tsx
// routes.tsx
{
  path: 'dashboard',
  element: <DashboardLayout />,
  children: [
    { index: true, element: <DashboardHome /> },
    {
      path: 'users',
      element: <UsersLayout />,
      children: [
        { index: true, element: <UsersList /> },
        { path: ':id', element: <UserDetails /> },
        { path: ':id/edit', element: <UserEdit /> },
      ],
    },
    { path: 'settings', element: <SettingsPage /> },
  ],
}

// DashboardLayout.tsx
import { Outlet } from 'react-router-dom';

export const DashboardLayout = () => {
  return (
    <div>
      <Sidebar />
      <main>
        <Outlet /> {/* Рендерит дочерний route */}
      </main>
    </div>
  );
};
```

## Data Loaders

```tsx
// loaders.ts
import { LoaderFunction } from 'react-router-dom';

export const userLoader: LoaderFunction = async ({ params }) => {
  const response = await fetch(`/api/users/${params.id}`);
  if (!response.ok) {
    throw new Response('User not found', { status: 404 });
  }
  return response.json();
};

// routes.tsx
{
  path: 'users/:id',
  loader: userLoader,
  element: <UserPage />,
  errorElement: <ErrorPage />,
}

// UserPage.tsx
import { useLoaderData } from 'react-router-dom';

export const UserPage = () => {
  const user = useLoaderData() as User;
  return <UserProfile user={user} />;
};
```

## Programmatic Navigation

```tsx
import { useNavigate, useLocation, Link } from 'react-router-dom';

// Навигация из компонента
export const LoginButton = () => {
  const navigate = useNavigate();
  const location = useLocation();
  
  const handleLogin = () => {
    // Переход после логина
    navigate('/dashboard', { replace: true });
    // Или с сохранением state
    navigate('/dashboard', { state: { from: location } });
  };

  return <button onClick={handleLogin}>Login</button>;
};

// Декларативная навигация
export const Navigation = () => (
  <nav>
    <Link to="/">Home</Link>
    <Link to="/profile" state={{ editMode: true }}>Profile</Link>
    <NavLink 
      to="/settings"
      className={({ isActive }) => isActive ? 'active' : ''}
    >
      Settings
    </NavLink>
  </nav>
);

// Получение location state
export const ProfilePage = () => {
  const { state } = useLocation();
  const editMode = state?.editMode;
  // ...
};
```

## Protected Routes

```tsx
// components/ProtectedRoute.tsx
import { Navigate, Outlet } from 'react-router-dom';
import { useAppSelector } from '@/store';

export const ProtectedRoute = () => {
  const isAuthenticated = useAppSelector(selectIsAuthenticated);
  const location = useLocation();

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <Outlet />;
};

// routes.tsx
{
  element: <ProtectedRoute />,
  children: [
    { path: 'dashboard', element: <DashboardPage /> },
    { path: 'profile', element: <ProfilePage /> },
  ],
}

// Для ролей
export const RoleRoute = ({ allowedRoles }: { allowedRoles: string[] }) => {
  const user = useAppSelector(selectCurrentUser);
  const location = useLocation();

  if (!user) return <Navigate to="/login" replace />;
  if (!allowedRoles.includes(user.role)) {
    return <Navigate to="/unauthorized" replace />;
  }

  return <Outlet />;
};
```

## URL Params

```tsx
import { useParams, useSearchParams } from 'react-router-dom';

// Path params
export const UserPage = () => {
  const { id } = useParams<{ id: string }>();
  // ...
};

// Query params
export const ProductList = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const category = searchParams.get('category');
  const page = searchParams.get('page') || '1';

  const handleCategoryChange = (cat: string) => {
    setSearchParams({ category: cat, page: '1' });
  };

  // ...
};
```
