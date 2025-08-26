import React from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Stack,
  Chip,
} from '@mui/material';
import {
  Favorite,
  LocationOn,
  Notifications,
  Psychology,
  Security,
  Speed,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const features = [
    {
      icon: <Speed sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'Quick Matching',
      description: 'Find compatible donors within minutes using our intelligent matching algorithm.',
    },
    {
      icon: <LocationOn sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'Location-Based',
      description: 'Connect with donors in your area for faster response times.',
    },
    {
      icon: <Psychology sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'AI-Powered',
      description: 'ML algorithms predict donor reliability for better matching success.',
    },
    {
      icon: <Notifications sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'Real-time Alerts',
      description: 'Instant SMS and email notifications for urgent requests.',
    },
    {
      icon: <Security sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'Secure & Private',
      description: 'Your personal information is protected with industry-standard security.',
    },
    {
      icon: <Favorite sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'Save Lives',
      description: 'Join our community of donors and help save lives every day.',
    },
  ];

  const stats = [
    { label: 'Donors Registered', value: '10,000+' },
    { label: 'Lives Saved', value: '50,000+' },
    { label: 'Cities Covered', value: '500+' },
    { label: 'Success Rate', value: '95%' },
  ];

  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          background: 'linear-gradient(135deg, #d32f2f 0%, #1976d2 100%)',
          color: 'white',
          py: 8,
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <Container maxWidth="lg">
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={6}>
              <Typography variant="h2" component="h1" gutterBottom fontWeight="bold">
                Connect Donors with Patients
              </Typography>
              <Typography variant="h5" paragraph sx={{ opacity: 0.9 }}>
                Our intelligent platform matches blood and organ donors with patients in need,
                making the donation process faster, safer, and more efficient.
              </Typography>
              <Stack direction="row" spacing={2} sx={{ mt: 4 }}>
                {!isAuthenticated ? (
                  <>
                    <Button
                      variant="contained"
                      size="large"
                      onClick={() => navigate('/register')}
                      sx={{
                        bgcolor: 'white',
                        color: 'primary.main',
                        '&:hover': { bgcolor: 'grey.100' },
                      }}
                    >
                      Get Started
                    </Button>
                    <Button
                      variant="outlined"
                      size="large"
                      onClick={() => navigate('/login')}
                      sx={{ borderColor: 'white', color: 'white' }}
                    >
                      Sign In
                    </Button>
                  </>
                ) : (
                  <Button
                    variant="contained"
                    size="large"
                    onClick={() => navigate('/dashboard')}
                    sx={{
                      bgcolor: 'white',
                      color: 'primary.main',
                      '&:hover': { bgcolor: 'grey.100' },
                    }}
                  >
                    Go to Dashboard
                  </Button>
                )}
              </Stack>
            </Grid>
            <Grid item xs={12} md={6}>
              <Box
                sx={{
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                  height: 400,
                }}
              >
                <Box
                  component="img"
                  src="/hero-image.png"
                  alt="Donation Matching"
                  sx={{
                    maxWidth: '100%',
                    height: 'auto',
                    filter: 'drop-shadow(0 10px 20px rgba(0,0,0,0.3))',
                  }}
                />
              </Box>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Stats Section */}
      <Box sx={{ py: 6, bgcolor: 'background.default' }}>
        <Container maxWidth="lg">
          <Grid container spacing={4}>
            {stats.map((stat, index) => (
              <Grid item xs={6} md={3} key={index}>
                <Box textAlign="center">
                  <Typography variant="h3" component="div" color="primary" fontWeight="bold">
                    {stat.value}
                  </Typography>
                  <Typography variant="body1" color="text.secondary">
                    {stat.label}
                  </Typography>
                </Box>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* Features Section */}
      <Box sx={{ py: 8 }}>
        <Container maxWidth="lg">
          <Typography variant="h3" component="h2" textAlign="center" gutterBottom>
            Why Choose Our Platform?
          </Typography>
          <Typography variant="h6" textAlign="center" color="text.secondary" paragraph>
            We combine cutting-edge technology with human compassion to make donation matching efficient and reliable.
          </Typography>
          
          <Grid container spacing={4} sx={{ mt: 4 }}>
            {features.map((feature, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <Card
                  sx={{
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    transition: 'transform 0.2s',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                    },
                  }}
                >
                  <CardContent sx={{ flexGrow: 1, textAlign: 'center', py: 4 }}>
                    <Box sx={{ mb: 2 }}>{feature.icon}</Box>
                    <Typography variant="h6" component="h3" gutterBottom>
                      {feature.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {feature.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* CTA Section */}
      <Box sx={{ py: 8, bgcolor: 'primary.main', color: 'white' }}>
        <Container maxWidth="md">
          <Box textAlign="center">
            <Typography variant="h3" component="h2" gutterBottom>
              Ready to Make a Difference?
            </Typography>
            <Typography variant="h6" paragraph sx={{ opacity: 0.9 }}>
              Join thousands of donors and patients who trust our platform for life-saving connections.
            </Typography>
            <Stack direction="row" spacing={2} justifyContent="center" sx={{ mt: 4 }}>
              <Button
                variant="contained"
                size="large"
                onClick={() => navigate('/donor/register')}
                sx={{
                  bgcolor: 'white',
                  color: 'primary.main',
                  '&:hover': { bgcolor: 'grey.100' },
                }}
              >
                Register as Donor
              </Button>
              <Button
                variant="outlined"
                size="large"
                onClick={() => navigate('/request/create')}
                sx={{ borderColor: 'white', color: 'white' }}
              >
                Create Request
              </Button>
            </Stack>
          </Box>
        </Container>
      </Box>

      {/* Footer */}
      <Box sx={{ py: 4, bgcolor: 'grey.900', color: 'white' }}>
        <Container maxWidth="lg">
          <Grid container spacing={4}>
            <Grid item xs={12} md={4}>
              <Typography variant="h6" gutterBottom>
                Blood & Organ Donation Matcher
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                Connecting donors with patients in need through intelligent matching technology.
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="h6" gutterBottom>
                Quick Links
              </Typography>
              <Stack spacing={1}>
                <Button color="inherit" onClick={() => navigate('/donor/search')}>
                  Find Donors
                </Button>
                <Button color="inherit" onClick={() => navigate('/request/create')}>
                  Create Request
                </Button>
                <Button color="inherit" onClick={() => navigate('/register')}>
                  Register
                </Button>
              </Stack>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="h6" gutterBottom>
                Contact
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                Email: support@donationmatcher.com<br />
                Phone: +1 (555) 123-4567<br />
                Emergency: 24/7 Support Available
              </Typography>
            </Grid>
          </Grid>
          <Box sx={{ mt: 4, pt: 2, borderTop: 1, borderColor: 'grey.800', textAlign: 'center' }}>
            <Typography variant="body2" sx={{ opacity: 0.6 }}>
              © 2024 Blood & Organ Donation Matcher. All rights reserved.
            </Typography>
          </Box>
        </Container>
      </Box>
    </Box>
  );
};

export default HomePage;