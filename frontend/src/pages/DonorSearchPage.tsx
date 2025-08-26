import React from 'react';
import { Box, Typography, Paper, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const DonorSearchPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Find Donors
      </Typography>
      <Paper sx={{ p: 3, textAlign: 'center' }}>
        <Typography variant="h6" gutterBottom>
          Search for Compatible Donors
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          This page will contain donor search functionality including:
        </Typography>
        <ul style={{ textAlign: 'left', display: 'inline-block' }}>
          <li>Blood group and location-based search</li>
          <li>Map view of nearby donors</li>
          <li>Donor reliability scores</li>
          <li>Contact and matching features</li>
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

export default DonorSearchPage;