import React from 'react';
import { Box, Typography, Paper, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const ProfilePage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Profile
      </Typography>
      <Paper sx={{ p: 3, textAlign: 'center' }}>
        <Typography variant="h6" gutterBottom>
          User Profile & Settings
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          This page will contain user profile management including:
        </Typography>
        <ul style={{ textAlign: 'left', display: 'inline-block' }}>
          <li>Personal information and contact details</li>
          <li>Donor profile (if applicable)</li>
          <li>Notification preferences</li>
          <li>Account settings and security</li>
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

export default ProfilePage;