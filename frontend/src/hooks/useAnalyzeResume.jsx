import { useState } from 'react';
import axios from 'axios';

export const useAnalyzeResume = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyzeResume = async (resumeUrl, jobDescription, jobRequirements) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('http://localhost:8888/api/ai/analyze-resume', {
        resume_url: resumeUrl,
        job_description: jobDescription,
        job_requirements: jobRequirements
      }, {
        withCredentials: true,
      });
      setData(response.data);

    } catch (err) {
      setError(err.response?.data?.message || 'An error occurred during analysis.');
      
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, analyzeResume };
};