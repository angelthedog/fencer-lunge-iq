import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { Container, Typography, Button, Box, Paper } from '@mui/material';
import FileUploadIcon from '@mui/icons-material/FileUpload';

const Home = () => {
  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 8, textAlign: 'center' }}>
        <Typography variant="h2" component="h1" gutterBottom>
          Welcome to FencerLunge
        </Typography>
        <Typography variant="h5" component="h2" gutterBottom color="text.secondary">
          Improve your fencing technique with AI-powered motion analysis
        </Typography>
        <Paper elevation={3} sx={{ p: 4, mt: 4, mb: 4 }}>
          <Typography variant="body1" paragraph>
            Upload your fencing lunge videos and get instant feedback on your technique.
            Our advanced AI system analyzes your form and provides detailed scoring based on
            body alignment, speed, and precision.
          </Typography>
          <Typography variant="body1" paragraph>
            Perfect for athletes, coaches, and enthusiasts looking to improve their performance.
          </Typography>
          <Button
            component={RouterLink}
            to="/upload"
            variant="contained"
            size="large"
            startIcon={<FileUploadIcon />}
            sx={{ mt: 2 }}
          >
            Start Analysis
          </Button>
        </Paper>
      </Box>
    </Container>
  );
};

export default Home;
