import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Button,
  Box,
  Paper,
  LinearProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Tabs,
  Tab,
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import VideocamIcon from '@mui/icons-material/Videocam';
import VideoCapture from '../components/VideoCapture';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`upload-tabpanel-${index}`}
      aria-labelledby={`upload-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

const Upload: React.FC = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [experience, setExperience] = useState('');
  const [notes, setNotes] = useState('');
  const [tabValue, setTabValue] = useState(0);
  const [accessToken, setAccessToken] = useState<string | null>(null);

  useEffect(() => {
    // Retrieve the access token from session storage when the component mounts
    const storedToken = sessionStorage.getItem('accessToken');
    setAccessToken(storedToken);
  }, []);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file || !accessToken) return;

    setUploading(true);

    try {
      const formData = new FormData();
      formData.append('video', file);
      formData.append('experience', experience);
      formData.append('notes', notes);

      const response = await fetch('http://localhost:8000/upload-video', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          // Don't set Content-Type here, it will be automatically set for FormData
        },
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Upload failed');
      }

      const result = await response.json();
      console.log('Upload successful:', result);
      navigate('/results');
    } catch (error) {
      console.error('Error uploading video:', error);
      // Handle error (e.g., show error message to user)
    } finally {
      setUploading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Upload Video
        </Typography>
        <Paper sx={{ mt: 2 }}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={tabValue} onChange={handleTabChange} aria-label="upload options">
              <Tab icon={<CloudUploadIcon />} label="File Upload" />
              <Tab icon={<VideocamIcon />} label="Record Video" />
            </Tabs>
          </Box>

          <Box sx={{ p: 2 }}>
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Experience Level</InputLabel>
              <Select
                value={experience}
                label="Experience Level"
                onChange={(e) => setExperience(e.target.value as string)}
              >
                <MenuItem value="beginner">Beginner</MenuItem>
                <MenuItem value="intermediate">Intermediate</MenuItem>
                <MenuItem value="advanced">Advanced</MenuItem>
              </Select>
            </FormControl>
            <TextField
              fullWidth
              label="Additional Notes"
              multiline
              rows={3}
              variant="outlined"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              sx={{ mb: 2 }}
            />
          </Box>

          <TabPanel value={tabValue} index={0}>
            <Box sx={{ textAlign: 'center' }}>
              <input
                accept="video/mp4,video/mov,video/webm"
                style={{ display: 'none' }}
                id="video-upload"
                type="file"
                onChange={handleFileSelect}
              />
              <label htmlFor="video-upload">
                <Button
                  variant="outlined"
                  component="span"
                  startIcon={<CloudUploadIcon />}
                  size="large"
                >
                  Select Video
                </Button>
              </label>
              
              {file && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="body1">
                    Selected file: {file.name}
                  </Typography>
                  <Button
                    variant="contained"
                    onClick={handleUpload}
                    disabled={uploading || !accessToken}
                    sx={{ mt: 2 }}
                  >
                    Upload and Analyze
                  </Button>
                  {uploading && (
                    <Box sx={{ mt: 2 }}>
                      <LinearProgress />
                    </Box>
                  )}
                </Box>
              )}
            </Box>
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <VideoCapture />
          </TabPanel>
        </Paper>
      </Box>
    </Container>
  );
};

export default Upload;
