import { useState, useEffect } from "react";
import axios from "axios";
import { AI_API_END_POINT } from "../utils/constant";

export const useMatchedJobs = () => {
  const [matches, setMatches]   = useState([]);
  const [loading, setLoading]   = useState(true);
  const [error, setError]       = useState("");

  useEffect(() => {
    (async () => {
      try {
        const { data } = await axios.get(`${AI_API_END_POINT}/match-jobs`, { withCredentials: true });
        console.log("AI matches response:", data);
        const jobArray = Array.isArray(data) ? data : data.matched_jobs ?? [];
        setMatches(jobArray);
      } catch (err) {
        setError(err.response?.data?.message || err.message);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return { matches, loading, error };
};