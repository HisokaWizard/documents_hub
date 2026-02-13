# Redux

## Содержание

1. [Redux Toolkit](#redux-toolkit)
2. [RTK Query](#rtk-query)
3. [Структура Store](#структура-store)
4. [Best Practices](#best-practices)

---

## Redux Toolkit

```tsx
// Создание slice
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UserState {
  currentUser: User | null;
  isAuthenticated: boolean;
}

const initialState: UserState = {
  currentUser: null,
  isAuthenticated: false,
};

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<User>) => {
      state.currentUser = action.payload;
      state.isAuthenticated = true;
    },
    logout: (state) => {
      state.currentUser = null;
      state.isAuthenticated = false;
    },
  },
});

export const { setUser, logout } = userSlice.actions;
export default userSlice.reducer;
```

## RTK Query

```tsx
// API slice
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const api = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  tagTypes: ['User', 'Post'],
  endpoints: (builder) => ({
    getUsers: builder.query<User[], void>({
      query: () => 'users',
      providesTags: ['User'],
    }),
    getUser: builder.query<User, string>({
      query: (id) => `users/${id}`,
      providesTags: (result, error, id) => [{ type: 'User', id }],
    }),
    createUser: builder.mutation<User, CreateUserDto>({
      query: (body) => ({
        url: 'users',
        method: 'POST',
        body,
      }),
      invalidatesTags: ['User'],
    }),
    updateUser: builder.mutation<User, { id: string; body: UpdateUserDto }>({
      query: ({ id, body }) => ({
        url: `users/${id}`,
        method: 'PUT',
        body,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: 'User', id }],
    }),
  }),
});

export const { useGetUsersQuery, useGetUserQuery, useCreateUserMutation, useUpdateUserMutation } = api;
```

## Структура Store

```tsx
// store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import { api } from './api';
import userReducer from './slices/userSlice';
import uiReducer from './slices/uiSlice';

export const store = configureStore({
  reducer: {
    [api.reducerPath]: api.reducer,
    user: userReducer,
    ui: uiReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(api.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// Typed hooks
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux';
export const useAppDispatch: () => AppDispatch = useDispatch;
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
```

## Best Practices

```tsx
// Использование в компоненте
const UserProfile = () => {
  const dispatch = useAppDispatch();
  const { data: user, isLoading, error } = useGetUserQuery('123');
  const [updateUser] = useUpdateUserMutation();

  const handleUpdate = async (values: UpdateUserDto) => {
    await updateUser({ id: user.id, body: values }).unwrap();
  };

  if (isLoading) return <Spinner />;
  if (error) return <Error />;
  return <UserForm user={user} onSubmit={handleUpdate} />;
};

// Selectors
const selectCurrentUser = (state: RootState) => state.user.currentUser;
const selectIsAuthenticated = (state: RootState) => state.user.isAuthenticated;

// Conditional fetching
const { data } = useGetUserQuery(userId, {
  skip: !userId, // Пропускаем если нет id
});

// Polling
const { data } = useGetNotificationsQuery(undefined, {
  pollingInterval: 30000, // Каждые 30 секунд
});
```

## Кэширование и Tags

```tsx
// Автоматическое обновление кэша
const api = createApi({
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  tagTypes: ['Post'],
  endpoints: (builder) => ({
    getPosts: builder.query<Post[], void>({
      query: () => 'posts',
      providesTags: (result) =>
        result
          ? [...result.map(({ id }) => ({ type: 'Post' as const, id })), 'Post']
          : ['Post'],
    }),
    addPost: builder.mutation<Post, Partial<Post>>({
      query: (body) => ({
        url: 'posts',
        method: 'POST',
        body,
      }),
      invalidatesTags: ['Post'], // Инвалидирует весь кэш posts
    }),
  }),
});
```
