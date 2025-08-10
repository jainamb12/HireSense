// components/user/UserProtectedRoute.jsx

import React, { useEffect } from 'react';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';

const UserProtectedRoute = ({ children }) => {
  const { user } = useSelector((store) => store.auth);
  const navigate = useNavigate();

  useEffect(() => {
    // If there is no user or the user's role is not 'student', redirect to the homepage
    if (!user || user.role !== 'student') {
      navigate('/');
    }
  }, [user, navigate]);

  return <>{children}</>;
};

export default UserProtectedRoute;