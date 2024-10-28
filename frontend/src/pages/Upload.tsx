import React, { useState } from 'react';
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
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

const Upload = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [experience, setExperience] = useState('');

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    // TODO: Implement actual upload logic with API call
    setTimeout(() => {
      setUploading(false);
      navigate('/results');
    }, 2000);
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Upload Video
        </Typography>
        <Paper sx={{ p: 4, mt: 2 }}>
          <Box sx={{ mb: 4 }}>
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Experience Level</InputLabel>
              <Select
                value={experience}
                label="Experience Level"
                onChange={(e) => setExperience(e.target.value)}
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
            />
          </Box>
          
          <Box sx={{ textAlign: 'center' }}>
            <input
              accept="video/mp4,video/mov"
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
                  disabled={uploading}
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
        </Paper>
      </Box>
    </Container>
  );
};

export default Upload;
