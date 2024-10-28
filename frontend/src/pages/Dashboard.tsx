import React from 'react';
import {
  Container,
  Typography,
  Paper,
  Box,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';

const Dashboard = () => {
  // Mock data - replace with actual API data
  const recentUploads = [
    {
      id: 1,
      date: '2024-01-15',
      score: 85,
      bodyAlignment: 90,
      speed: 82,
      precision: 88,
    },
    {
      id: 2,
      date: '2024-01-14',
      score: 82,
      bodyAlignment: 85,
      speed: 80,
      precision: 84,
    },
    {
      id: 3,
      date: '2024-01-13',
      score: 78,
      bodyAlignment: 80,
      speed: 75,
      precision: 82,
    },
  ];

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Your Dashboard
        </Typography>
        
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Performance Overview
              </Typography>
              <Typography variant="body1" color="text.secondary" paragraph>
                Your average score has improved by 7% over the last 3 sessions
              </Typography>
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Recent Analyses
              </Typography>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Date</TableCell>
                      <TableCell align="right">Overall Score</TableCell>
                      <TableCell align="right">Body Alignment</TableCell>
                      <TableCell align="right">Speed</TableCell>
                      <TableCell align="right">Precision</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {recentUploads.map((upload) => (
                      <TableRow key={upload.id}>
                        <TableCell component="th" scope="row">
                          {upload.date}
                        </TableCell>
                        <TableCell align="right">{upload.score}</TableCell>
                        <TableCell align="right">{upload.bodyAlignment}%</TableCell>
                        <TableCell align="right">{upload.speed}%</TableCell>
                        <TableCell align="right">{upload.precision}%</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default Dashboard;
