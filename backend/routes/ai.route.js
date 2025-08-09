import express from "express";
import { matchJobs } from "../controllers/ai.controller.js";
import isAuthenticated from "../middlewares/isAuthenticated.js";
import { analyzeResumeFit } from '../controllers/ai.controller.js';

const router = express.Router();
router.get("/match-jobs", isAuthenticated, matchJobs);
router.post('/analyze-resume', isAuthenticated, analyzeResumeFit);

export default router;
