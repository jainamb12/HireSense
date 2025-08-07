// import axios from "axios";
// import { Job } from "../models/job.model.js";
// import { User } from "../models/user.model.js";

// const AI_BASE = "http://127.0.0.1:8000";

// export const matchJobs = async (req, res, next) => {
//   try {
//     // 1️⃣ current logged‑in user (assumes auth middleware sets req.user)
//     const userId = req.id;

//     // 2️⃣ fetch résumé URL from nested profile.resume
//     const user = await User.findById(userId).select("profile.resume");
//     const resumeUrl = user?.profile?.resume;
//     if (!resumeUrl)
//       return res.status(400).json({ message: "Please upload your résumé first." });

//     // 3️⃣ fetch open jobs & populate company name
//     const jobs = await Job.find({})
//   .select("_id title description requirements salary position jobType company")
//   .populate("company", "name logo");

// const payloadJobs = jobs.map(j => ({
//   id: j.id.toString(),
//   _id: j.id.toString(),             // 👈 ensure string
//   title: j.title,
//   description: j.description,
//   requirements: j.requirements,
//   salary: j.salary,
//   position: j.position,
//   jobType: j.jobType,
//   createdAt: j.createdAt,
//   company: {
//     name: j.company?.name || "Unknown",
//     logo: j.company?.logo || ""
//   }
// }));


//     // 5️⃣ call FastAPI
//     const { data } = await axios.post(`${AI_BASE}/match-jobs`, {
//       resume_url: resumeUrl,
//       jobs: payloadJobs
//     });

//     // console.log("UserId:", userId);
//     // console.log("DB user document:", user);
//     // console.log("DB jobs document:", jobs);

//     return res.json(data.matched_jobs.slice(0,6));      // send to React
//   } catch (err) {
//     next(err);
//   }
// };



import axios from "axios";
import { Job } from "../models/job.model.js"; // Make sure this path is correct for your Job Mongoose model
import { User } from "../models/user.model.js";

const AI_BASE = "http://127.0.0.1:8000";

export const matchJobs = async (req, res, next) => {
  try {
    const userId = req.id;

    const user = await User.findById(userId).select("profile.resume");
    const resumeUrl = user?.profile?.resume;
    if (!resumeUrl)
      return res.status(400).json({ message: "Please upload your résumé first." });

    // 3️⃣ fetch open jobs & populate company name
    const jobs = await Job.find({})
      // Select all fields that are going to be sent to FastAPI.
      // Also ensure you populate 'company' for its 'name' and 'logo' (if logo is available in Company model)
      .select("_id title description requirements salary experienceLevel location jobType position company createdAt") // Added missing fields
      .populate("company", "name logo"); // Assuming Company model has a 'name' and 'logo' field

    const payloadJobs = jobs.map(j => ({
      _id: j._id.toString(), // Mongoose documents have _id by default. Use ._id not .id for consistency with your previous code
      title: j.title,
      description: j.description,
      requirements: j.requirements,
      salary: j.salary, // Mongoose `Number` will be a JavaScript number
      experienceLevel: j.experienceLevel, // New field, ensure it's a number
      location: j.location, // New field, ensure it's a string
      jobType: j.jobType,
      position: j.position, // Mongoose `Number` will be a JavaScript number
      createdAt: j.createdAt ? j.createdAt.toISOString() : null, // Mongoose Date object to ISO string
      company: {
        name: j.company?.name || "Unknown",
        logo: j.company?.logo || "" // Include logo if populated
      }
      // Do NOT include fields here that are not in your Pydantic Job model
      // (e.g., created_by, applications, updatedAt, etc.)
    }));

    // 5️⃣ call FastAPI
    const { data } = await axios.post(`${AI_BASE}/match-jobs`, {
      resume_url: resumeUrl,
      jobs: payloadJobs
    });

    // console.log("UserId:", userId);
    // console.log("DB user document:", user);
    // console.log("DB jobs document:", jobs);
    // console.log("Payload sent to FastAPI:", JSON.stringify(payloadJobs, null, 2)); // Add this for debugging

    return res.json(data.matched_jobs.slice(0, 6));
  } catch (err) {
    if (axios.isAxiosError(err) && err.response) {
      console.error("FastAPI Validation Error Response:", err.response.data);
      // Return the detailed error from FastAPI for better debugging on the client-side
      return res.status(err.response.status).json(err.response.data);
    } else {
      console.error("Other Error:", err);
    }
    next(err);
  }
};