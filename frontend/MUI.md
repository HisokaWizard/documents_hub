# MUI

## Содержание

1. [Темизация](#темизация)
2. [Компоненты](#компоненты)
3. [Стилизация](#стилизация)
4. [Best Practices](#best-practices)

---

## Темизация

```tsx
// theme.ts
import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#1565c0',
    },
    secondary: {
      main: '#dc004e',
    },
  },
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
    h1: { fontSize: '2.5rem', fontWeight: 500 },
    h2: { fontSize: '2rem', fontWeight: 500 },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
        },
      },
    },
  },
});

// App.tsx
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

export const App = () => (
  <ThemeProvider theme={theme}>
    <CssBaseline />
    <RouterProvider router={router} />
  </ThemeProvider>
);
```

## Компоненты

```tsx
// Layout
import { Box, Container, Grid, Stack } from '@mui/material';

export const Layout = () => (
  <Container maxWidth="lg">
    <Grid container spacing={3}>
      <Grid item xs={12} md={8}>
        <MainContent />
      </Grid>
      <Grid item xs={12} md={4}>
        <Sidebar />
      </Grid>
    </Grid>
  </Container>
);

// Forms
import { TextField, Button, FormControl, InputLabel, Select, MenuItem } from '@mui/material';

export const UserForm = () => {
  const [value, setValue] = useState('');
  
  return (
    <Stack spacing={2}>
      <TextField
        label="Name"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        variant="outlined"
        fullWidth
      />
      <Button variant="contained" color="primary">
        Submit
      </Button>
    </Stack>
  );
};

// Feedback
import { Alert, Snackbar, CircularProgress, Skeleton } from '@mui/material';

export const LoadingState = () => (
  <>
    <CircularProgress />
    <Skeleton variant="rectangular" width={210} height={118} />
  </>
);

export const ErrorAlert = ({ message }: { message: string }) => (
  <Snackbar open autoHideDuration={6000}>
    <Alert severity="error">{message}</Alert>
  </Snackbar>
);
```

## Стилизация

```tsx
// sx prop
<Box
  sx={{
    display: 'flex',
    gap: 2,
    p: 2,
    bgcolor: 'background.paper',
    borderRadius: 1,
    '&:hover': { bgcolor: 'action.hover' },
  }}
>
  Content
</Box>

// styled API
import { styled } from '@mui/material/styles';

const StyledCard = styled(Card)(({ theme }) => ({
  padding: theme.spacing(2),
  marginBottom: theme.spacing(2),
  boxShadow: theme.shadows[3],
  [theme.breakpoints.down('sm')]: {
    padding: theme.spacing(1),
  },
}));

// useTheme hook
import { useTheme } from '@mui/material/styles';

export const ResponsiveComponent = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  
  return <Box padding={isMobile ? 1 : 3}>Content</Box>;
};
```

## Best Practices

```tsx
// Responsive design
import { useMediaQuery, useTheme } from '@mui/material';

export const ResponsiveLayout = () => {
  const theme = useTheme();
  const isTablet = useMediaQuery(theme.breakpoints.down('md'));
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  return (
    <Grid container spacing={isMobile ? 1 : 3}>
      <Grid item xs={12} md={isTablet ? 12 : 8}>
        Main
      </Grid>
    </Grid>
  );
};

// Loading states
import { Skeleton } from '@mui/material';

export const UserCard = ({ user, loading }: { user?: User; loading: boolean }) => {
  if (loading) {
    return (
      <Card>
        <Skeleton variant="circular" width={40} height={40} />
        <Skeleton variant="text" width="60%" />
        <Skeleton variant="text" width="40%" />
      </Card>
    );
  }
  return <Card>{user?.name}</Card>;
};

// Form validation
<TextField
  error={Boolean(errors.email)}
  helperText={errors.email?.message}
  {...register('email', { required: 'Email is required' })}
/>

// Icons
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';

<Button startIcon={<AddIcon />}>Add</Button>
<IconButton color="error"><DeleteIcon /></IconButton>
```
