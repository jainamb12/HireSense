import express from "express";
import { getJobAnalytics, matchJobs } from "../controllers/ai.controller.js";
import isAuthenticated from "../middlewares/isAuthenticated.js";
import { analyzeResumeFit } from '../controllers/ai.controller.js';

const router = express.Router();
router.get("/match-jobs", isAuthenticated, matchJobs);
router.post('/analyze-resume', isAuthenticated, analyzeResumeFit);
router.get('/job-analytics', isAuthenticated, getJobAnalytics);

export default router;
