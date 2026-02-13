# Testing

## Содержание

1. [Unit Testing](#unit-testing)
2. [Component Testing](#component-testing)
3. [E2E Testing](#e2e-testing)
4. [Best Practices](#best-practices)

---

## Unit Testing

```tsx
// utils.test.ts
import { formatDate, calculateTotal } from './utils';

describe('formatDate', () => {
  it('should format date correctly', () => {
    const date = new Date('2024-01-15');
    expect(formatDate(date)).toBe('15.01.2024');
  });

  it('should handle invalid date', () => {
    expect(formatDate(null)).toBe('');
  });
});

// hooks.test.ts
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('should increment counter', () => {
    const { result } = renderHook(() => useCounter());
    
    act(() => {
      result.current.increment();
    });
    
    expect(result.current.count).toBe(1);
  });
});
```

## Component Testing

```tsx
// Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from './Button';

describe('Button', () => {
  it('should render button with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('should handle click', async () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    
    await userEvent.click(screen.getByText('Click'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('should be disabled when loading', () => {
    render(<Button isLoading>Submit</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});

// Form.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UserForm } from './UserForm';

describe('UserForm', () => {
  it('should submit form with valid data', async () => {
    const onSubmit = jest.fn();
    render(<UserForm onSubmit={onSubmit} />);
    
    await userEvent.type(screen.getByLabelText('Name'), 'John');
    await userEvent.type(screen.getByLabelText('Email'), 'john@example.com');
    await userEvent.click(screen.getByRole('button', { name: /submit/i }));
    
    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        name: 'John',
        email: 'john@example.com',
      });
    });
  });

  it('should show validation errors', async () => {
    render(<UserForm onSubmit={jest.fn()} />);
    await userEvent.click(screen.getByRole('button', { name: /submit/i }));
    
    expect(screen.getByText('Name is required')).toBeInTheDocument();
  });
});

// Redux testing
import { renderWithProviders } from '@/test-utils';
import { UserList } from './UserList';

describe('UserList', () => {
  it('should render users from store', () => {
    const preloadedState = {
      users: {
        items: [{ id: '1', name: 'John' }],
      },
    };
    
    renderWithProviders(<UserList />, { preloadedState });
    expect(screen.getByText('John')).toBeInTheDocument();
  });
});
```

## E2E Testing

```tsx
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
  ],
});

// e2e/auth.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('should login successfully', async ({ page }) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'user@example.com');
    await page.fill('[name="password"]', 'password');
    await page.click('button[type="submit"]');
    
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('text=Welcome')).toBeVisible();
  });

  test('should show error on invalid credentials', async ({ page }) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'wrong@example.com');
    await page.fill('[name="password"]', 'wrong');
    await page.click('button[type="submit"]');
    
    await expect(page.locator('text=Invalid credentials')).toBeVisible();
  });
});

// e2e/critical-flow.spec.ts
test.describe('Critical User Flow', () => {
  test('complete purchase flow', async ({ page }) => {
    await page.goto('/products');
    await page.click('text=Product 1');
    await page.click('text=Add to Cart');
    await page.click('text=Checkout');
    await page.fill('[name="card"]', '4242424242424242');
    await page.click('text=Pay');
    
    await expect(page.locator('text=Order confirmed')).toBeVisible();
  });
});
```

## Best Practices

```tsx
// Test utilities
// test-utils.tsx
import { render } from '@testing-library/react';
import { Provider } from 'react-redux';
import { ThemeProvider } from '@mui/material';
import { store } from '@/store';
import { theme } from '@/theme';

export function renderWithProviders(
  ui: React.ReactElement,
  { preloadedState = {}, ...renderOptions } = {}
) {
  function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <Provider store={store}>
        <ThemeProvider theme={theme}>
          {children}
        </ThemeProvider>
      </Provider>
    );
  }
  return { ...render(ui, { wrapper: Wrapper, ...renderOptions }) };
}

// Testing library queries
// Предпочитайте семантичные queries
screen.getByRole('button', { name: /submit/i }); // ✅ Лучше всего
screen.getByLabelText('Email'); // ✅ Хорошо
screen.getByTestId('submit-btn'); // ⚠️ Крайний случай

// Async testing
await waitFor(() => {
  expect(screen.getByText('Loaded')).toBeInTheDocument();
});

await waitForElementToBeRemoved(screen.queryByText('Loading'));

// Mocking
jest.mock('@/api', () => ({
  fetchUser: jest.fn().mockResolvedValue({ id: '1', name: 'John' }),
}));
```
