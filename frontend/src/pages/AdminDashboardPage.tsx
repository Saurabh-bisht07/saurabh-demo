import React from 'react';
import { Box, Typography, Paper, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const AdminDashboardPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Admin Dashboard
      </Typography>
      <Paper sx={{ p: 3, textAlign: 'center' }}>
        <Typography variant="h6" gutterBottom>
          Administrative Controls
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          This page will contain admin functionality including:
        </Typography>
        <ul style={{ textAlign: 'left', display: 'inline-block' }}>
          <li>System statistics and analytics</li>
          <li>User management and moderation</li>
          <li>ML model training and monitoring</li>
          <li>System configuration and settings</li>
        </ul>
        <Button
          variant="contained"
          onClick={() => navigate('/dashboard')}
          sx={{ mt: 2 }}
        >
          Back to Dashboard
        </Button>
      </Paper>
    </Box>
  );
};

export default AdminDashboardPage;