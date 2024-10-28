import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import Home from '../pages/Home';
import Login from './Login';

const AuthenticatedHome: React.FC = () => {
  const { user } = useAuth();

  return user ? <Home /> : <Login />;
};

export default AuthenticatedHome;
