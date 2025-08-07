import React, { useEffect } from 'react';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  const { user } = useSelector((store) => store.auth);
  const navigate  = useNavigate();

  useEffect(() => {
    if (!user || user.role !== 'recruiter') {
      navigate('/');
    }
  }, [user, navigate]);

  return <>{children}</>;
};

export default ProtectedRoute;