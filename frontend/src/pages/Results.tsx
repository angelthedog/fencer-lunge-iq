import React from 'react';
import {
  Container,
  Typography,
  Paper,
  Box,
  Grid,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  Divider,
} from '@mui/material';

const Results = () => {
  // Mock data - replace with actual API data
  const scores = {
    overall: 85,
    bodyAlignment: 90,
    speed: 82,
    precision: 88,
  };

  const feedback = [
    "Excellent body alignment throughout the lunge",
    "Speed could be improved in the recovery phase",
    "Good precision in target acquisition",
    "Maintain more consistent balance during execution",
  ];

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Analysis Results
        </Typography>
        
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Overall Score
              </Typography>
              <Typography variant="h2" color="primary" align="center">
                {scores.overall}
              </Typography>
            </Paper>
          </Grid>

          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Body Alignment
              </Typography>
              <Typography variant="h4" color="primary" align="center">
                {scores.bodyAlignment}%
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={scores.bodyAlignment} 
                sx={{ mt: 2 }}
              />
            </Paper>
          </Grid>

          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Speed
              </Typography>
              <Typography variant="h4" color="primary" align="center">
                {scores.speed}%
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={scores.speed} 
                sx={{ mt: 2 }}
              />
            </Paper>
          </Grid>

          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Precision
              </Typography>
              <Typography variant="h4" color="primary" align="center">
                {scores.precision}%
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={scores.precision} 
                sx={{ mt: 2 }}
              />
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Detailed Feedback
              </Typography>
              <List>
                {feedback.map((item, index) => (
                  <React.Fragment key={index}>
                    <ListItem>
                      <ListItemText primary={item} />
                    </ListItem>
                    {index < feedback.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default Results;
