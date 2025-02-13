# FencerLunge

A web application for analyzing fencing lunge performance using motion capture and machine learning.

## Project Structure

```
fencer-lunge/
├── frontend/          # React TypeScript frontend
├── backend/           # FastAPI Python backend
└── README.md
```

## Getting Started

### Frontend Development

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

### Backend Development

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   poetry config virtualenvs.in-project true # config local venv
   poetry shell # start the local .venv
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

### MongoDB database - use x.g@g SSO

### Repo in angelthedog github
1. fencer-lunge-iq - this repo for UI and BE
2. 3d_lunge_iq - python repo to build NN model and train
3. YoutubeVideooUpload - google SSO to upload fencing video to YT.
4. FencingLunge - old python repo to analyze lunge in 2D

## Features

- Video upload and processing
- Motion analysis using deepmotion.com Animate3D API
- Performance scoring and feedback
- User dashboard with historical data
- Google SSO authentication

## Technology Stack

- Frontend: React with TypeScript
- Backend: FastAPI (Python)
- Database: MongoDB
- Authentication: Google SSO
- Storage: Cloud storage for animation data
- API Integration: deepmotion.com Animate3D API

## Development Phases

1. Setup and Prototyping (Current)
2. Core Functionality
3. Advanced Features
4. Testing and Optimization
5. Deployment and Maintenance
