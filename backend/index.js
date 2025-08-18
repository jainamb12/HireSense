//const express = require('express')  old way
import express from 'express';
import cookieParser from 'cookie-parser';
import cors from 'cors';
import dotenv from 'dotenv';
import connectDB from './utils/db.js';
import userRoute from "./routes/user.route.js";
import companyRoute from "./routes/company.route.js";
import jobRoute from "./routes/job.route.js";
import applicationRoute from "./routes/application.route.js";
import aiRoutes from "./routes/ai.route.js";
dotenv.config({});

const app = express();

// middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());

app.use(cors({
  origin: process.env.FRONTEND_URL,
  credentials: true
}));

const PORT = process.env.PORT || 3000;

// api's
app.use("/api/v1/users", userRoute);
app.use("/api/v1/company", companyRoute);
app.use("/api/v1/job", jobRoute);
app.use("/api/v1/application", applicationRoute);
app.use("/api/ai", aiRoutes);

// "http://localhost:8000/api/v1/user/register"
// "http://localhost:8000/api/v1/user/login"
// "http://localhost:8000/api/v1/user/profile/update"

app.listen(PORT, () => {
    connectDB();
    console.log(`Server is running on port ${PORT}`);
})