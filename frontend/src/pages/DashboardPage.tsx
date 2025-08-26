import React from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Stack,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  Add,
  Search,
  List,
  Person,
  Favorite,
  TrendingUp,
  Notifications,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  const quickActions = [
    {
      title: 'Find Donors',
      description: 'Search for compatible donors in your area',
      icon: <Search sx={{ fontSize: 40 }} />,
      action: () => navigate('/donor/search'),
      color: 'primary',
    },
    {
      title: 'Create Request',
      description: 'Post a new donation request',
      icon: <Add sx={{ fontSize: 40 }} />,
      action: () => navigate('/request/create'),
      color: 'secondary',
    },
    {
      title: 'My Requests',
      description: 'View and manage your donation requests',
      icon: <List sx={{ fontSize: 40 }} />,
      action: () => navigate('/requests'),
      color: 'success',
    },
    {
      title: 'Profile',
      description: 'Update your profile and preferences',
      icon: <Person sx={{ fontSize: 40 }} />,
      action: () => navigate('/profile'),
      color: 'info',
    },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Welcome back, {user?.full_name}!
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Here's what's happening with your donation matching activities.
      </Typography>

      {/* Quick Actions */}
      <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
        Quick Actions
      </Typography>
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {quickActions.map((action, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card
              sx={{
                height: '100%',
                cursor: 'pointer',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                },
              }}
              onClick={action.action}
            >
              <CardContent sx={{ textAlign: 'center', py: 3 }}>
                <Box sx={{ color: `${action.color}.main`, mb: 2 }}>
                  {action.icon}
                </Box>
                <Typography variant="h6" gutterBottom>
                  {action.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {action.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Statistics */}
      <Typography variant="h5" gutterBottom>
        Your Statistics
      </Typography>
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Total Requests
              </Typography>
              <Typography variant="h4" component="div">
                12
              </Typography>
              <LinearProgress variant="determinate" value={70} sx={{ mt: 1 }} />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Successful Matches
              </Typography>
              <Typography variant="h4" component="div">
                8
              </Typography>
              <LinearProgress variant="determinate" value={80} sx={{ mt: 1 }} />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Active Requests
              </Typography>
              <Typography variant="h4" component="div">
                3
              </Typography>
              <LinearProgress variant="determinate" value={30} sx={{ mt: 1 }} />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Response Rate
              </Typography>
              <Typography variant="h4" component="div">
                95%
              </Typography>
              <LinearProgress variant="determinate" value={95} sx={{ mt: 1 }} />
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Recent Activity */}
      <Typography variant="h5" gutterBottom>
        Recent Activity
      </Typography>
      <Card>
        <CardContent>
          <Stack spacing={2}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Notifications color="primary" />
              <Box sx={{ flexGrow: 1 }}>
                <Typography variant="body1">
                  New donor match found for your A+ blood request
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  2 hours ago
                </Typography>
              </Box>
              <Chip label="New" color="success" size="small" />
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Favorite color="secondary" />
              <Box sx={{ flexGrow: 1 }}>
                <Typography variant="body1">
                  Your donation request was completed successfully
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  1 day ago
                </Typography>
              </Box>
              <Chip label="Completed" color="primary" size="small" />
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <TrendingUp color="success" />
              <Box sx={{ flexGrow: 1 }}>
                <Typography variant="body1">
                  Donor reliability score updated
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  3 days ago
                </Typography>
              </Box>
              <Chip label="Updated" color="info" size="small" />
            </Box>
          </Stack>
        </CardContent>
      </Card>
    </Box>
  );
};

export default DashboardPage;