import React from 'react';
import { Box, Typography, Paper, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const RequestCreatePage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Create Donation Request
      </Typography>
      <Paper sx={{ p: 3, textAlign: 'center' }}>
        <Typography variant="h6" gutterBottom>
          Request Blood or Organ Donation
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          This page will contain a request creation form including:
        </Typography>
        <ul style={{ textAlign: 'left', display: 'inline-block' }}>
          <li>Blood group and organ requirements</li>
          <li>Urgency level and timeline</li>
          <li>Location and hospital information</li>
          <li>Contact details and description</li>
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

export default RequestCreatePage;