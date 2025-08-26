import React from 'react';
import { Box, Typography, Paper, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const DonorRegistrationPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Donor Registration
      </Typography>
      <Paper sx={{ p: 3, textAlign: 'center' }}>
        <Typography variant="h6" gutterBottom>
          Register as a Blood/Organ Donor
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          This page will contain a comprehensive form for donor registration including:
        </Typography>
        <ul style={{ textAlign: 'left', display: 'inline-block' }}>
          <li>Blood group and donation preferences</li>
          <li>Location and contact information</li>
          <li>Medical history and eligibility</li>
          <li>Availability settings</li>
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

export default DonorRegistrationPage;