import { Job } from "../models/job.model.js";


// hosted by admin
export const postJob = async (req, res) => {
    try{
        const {title, description, requirements, salary, location, jobType, experienceLevel, position, company } = req.body;
        const userId = req.id;

        if(!title || !description || !requirements || !salary || !location || !jobType || !experienceLevel || !position || !company){
            return res.status(400).json({
                message: "Please fill in all fields.",
                success:false
            })
        };

        const job = await Job.create({
            title,
            description,
            requirements,
            salary:Number(salary),
            location,
            jobType,
            experienceLevel,
            position,
            company,
            created_by:userId
        });

        return res.status(201).json({
            message: "Job posted successfully",
            job,
            success:true,
        })
    }
    catch (error){
        console.log(error);
    }
}

// for job seekers
export const getAllJobs = async (req, res) => {
    try{
        const keyword = req.query.keyword || "";
        const query = {
            $or:[
                {title:{$regex:keyword,$options:"i"} },
                {description:{$regex:keyword,$options:"i"} },
            ]
        };

        //const jobs = await Job.find(query);  this will give only id of company and user not all information
        const jobs = await Job.find(query).populate({path:"company"}).sort({createdAt:-1});

        if(!jobs){
            return res.status(404).json({
                message: "No jobs found",
                success:false
            })
        };

        return res.status(200).json({
            jobs,
            success:true
        })
    }
    catch (error){
        console.log(error);
    }
}

// for job seekers
export const getJobById = async (req, res) => {
    try{
        const jobId = req.params.id;
        const job = await Job.findById(jobId).populate({
            path:"applications"
        });
        //const job = await Job.findById(jobId).populate("companyId").populate("created_by");
        if(!job){
            return res.status(404).json({
                message: "Job not found",
                success:false
            })
        };

        return res.status(200).json({
            job,
            success:true
        })
    }
    catch (error) {
        console.log(error);
    }
}


// how many jobs has been created by admin till now
export const getAdminJobs = async (req, res) => {
    try{
        const adminId = req.id;
        const jobs = await Job.find({created_by: adminId}).populate({
            path: "company",
            createdAt:-1
        });

        if(!jobs){
            return res.status(404).json({
                message: "No jobs found",
                success:false
            })
        };
        return res.status(200).json({
            jobs,
            success:true
        })
    }
    catch (error){
        console.log(error);
    }
}