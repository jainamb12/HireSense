// hooks/useJobAnalytics.js

import { useState, useEffect } from 'react';
import axios from 'axios';

export const useJobAnalytics = (location, job_type) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await axios.get('http://localhost:8888/api/ai/job-analytics', {
          params: { location, job_type },
          withCredentials: true,
        });
        setData(response.data);
      } catch (err) {
        console.error("Error fetching analytics:", err.response?.data || err.message);
        setError('Failed to fetch analytics data.');
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, [location, job_type]); // Fetch data whenever the filters change

  return { data, loading, error };
};