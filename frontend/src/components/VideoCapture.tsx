import React, { useRef, useState, useEffect } from 'react';
import { Button, Box, Typography } from '@mui/material';
import { useAuth } from '../contexts/AuthContext';

const VideoCapture: React.FC = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [error, setError] = useState<string>('');
  const { user } = useAuth();

  useEffect(() => {
    initializeCamera();
    return () => {
      stopMediaTracks();
    };
  }, []);

  const initializeCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: 'environment', // Use the back camera
          width: { ideal: 1280 },
          height: { ideal: 720 }
        },
        audio: true
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      setError('Failed to access camera. Please ensure you have granted camera permissions.');
      console.error('Error accessing camera:', err);
    }
  };

  const stopMediaTracks = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const tracks = (videoRef.current.srcObject as MediaStream).getTracks();
      tracks.forEach(track => track.stop());
    }
  };

  const startRecording = () => {
    if (!videoRef.current?.srcObject) return;

    const mediaStream = videoRef.current.srcObject as MediaStream;
    const mediaRecorder = new MediaRecorder(mediaStream, {
      mimeType: 'video/webm;codecs=vp9'
    });

    const chunks: Blob[] = [];
    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        chunks.push(event.data);
      }
    };

    mediaRecorder.onstop = async () => {
      const blob = new Blob(chunks, { type: 'video/webm' });
      await uploadVideo(blob);
    };

    mediaRecorderRef.current = mediaRecorder;
    mediaRecorder.start();
    setIsRecording(true);
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const uploadVideo = async (blob: Blob) => {
    if (!user) return;

    const formData = new FormData();
    formData.append('video', blob, 'recording.webm');

    try {
      const response = await fetch('http://localhost:8000/upload-video', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${user.access_token}`
        },
        body: formData
      });

      if (!response.ok) {
        throw new Error('Failed to upload video');
      }

      console.log('Video uploaded successfully');
    } catch (err) {
      console.error('Error uploading video:', err);
      setError('Failed to upload video. Please try again.');
    }
  };

  return (
    <Box sx={{ p: 2, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          {error}
        </Typography>
      )}
      
      <video
        ref={videoRef}
        autoPlay
        playsInline
        muted
        style={{
          width: '100%',
          maxWidth: '600px',
          borderRadius: '8px',
          marginBottom: '16px'
        }}
      />

      <Box sx={{ display: 'flex', gap: 2 }}>
        {!isRecording ? (
          <Button
            variant="contained"
            color="primary"
            onClick={startRecording}
          >
            Start Recording
          </Button>
        ) : (
          <Button
            variant="contained"
            color="error"
            onClick={stopRecording}
          >
            Stop Recording
          </Button>
        )}
      </Box>
    </Box>
  );
};

export default VideoCapture;
