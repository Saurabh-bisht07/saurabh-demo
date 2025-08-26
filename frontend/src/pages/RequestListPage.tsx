import React from 'react';
import { Box, Typography, Paper, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const RequestListPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        My Requests
      </Typography>
      <Paper sx={{ p: 3, textAlign: 'center' }}>
        <Typography variant="h6" gutterBottom>
          Manage Your Donation Requests
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          This page will display and manage your requests including:
        </Typography>
        <ul style={{ textAlign: 'left', display: 'inline-block' }}>
          <li>List of all your donation requests</li>
          <li>Request status and progress tracking</li>
          <li>Donor matches and contact information</li>
          <li>Request editing and completion</li>
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

export default RequestListPage;