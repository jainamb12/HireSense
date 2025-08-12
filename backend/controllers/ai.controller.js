import axios from "axios";
import { Job } from "../models/job.model.js";
import { User } from "../models/user.model.js";

const AI_BASE = "http://127.0.0.1:8000";

export const matchJobs = async (req, res, next) => {
  try {
    const userId = req.id;

    const user = await User.findById(userId).select("profile.resume");
    const resumeUrl = user?.profile?.resume;
    if (!resumeUrl)
      return res.status(400).json({ message: "Please upload your résumé first." });

    const jobs = await Job.find({})
      .select("_id title description requirements salary experienceLevel location jobType position company createdAt")
      .populate("company", "name logo");

    const payloadJobs = jobs.map(j => ({
      _id: j._id.toString(),
      title: j.title,
      description: j.description,
      requirements: j.requirements,
      salary: j.salary,
      experienceLevel: j.experienceLevel,
      location: j.location,
      jobType: j.jobType,
      position: j.position,
      createdAt: j.createdAt ? j.createdAt.toISOString() : null,
      company: {
        name: j.company?.name || "Unknown",
        logo: j.company?.logo || ""
      }
    }));

    // call FastAPI
    const { data } = await axios.post(`${AI_BASE}/match-jobs`, {
      resume_url: resumeUrl,
      jobs: payloadJobs
    });

    return res.json(data.matched_jobs.slice(0, 6));
  } catch (err) {
    if (axios.isAxiosError(err) && err.response) {
      console.error("FastAPI Validation Error Response:", err.response.data);
      return res.status(err.response.status).json(err.response.data);
    } else {
      console.error("Other Error:", err);
    }
    next(err);
  }
};


export const analyzeResumeFit = async (req, res, next) => {
  try {
    const { resume_url, job_description } = req.body;

    if (!resume_url || !job_description) {
      return res.status(400).json({ message: "Resume URL and job description are required." });
    }

    // Call the new FastAPI endpoint
    const { data } = await axios.post(`${AI_BASE}/analyze-resume-fit`, {
      resume_url,
      job_description,
    });

    return res.json(data);
  } catch (err) {
    console.error("FastAPI Error:", err.response?.data || err.message);

    // Pass the error to the next middleware
    next(err); 
  }
};


export const getJobAnalytics = async (req, res, next) => {
  try {
    const { location, job_type } = req.query;

    // Call the FastAPI analytics endpoint with the filters
    const { data } = await axios.get(`${AI_BASE}/job-analytics`, {
      params: {
        location,
        job_type,
      },
    });

    return res.json(data);
  } catch (err) {
    console.error("FastAPI Analytics Error:", err.response?.data || err.message);
    next(err); 
  }
};