import { User } from "../models/user.model.js";
import jwt from "jsonwebtoken";
import bcrypt from "bcryptjs";
import getDataUri from "../utils/datauri.js";
import cloudinary from "../utils/cloudinary.js";


export const register = async (req, res) => {
    try{
        const {fullname, email, phoneNumber, password, role} = req.body;
        console.log(fullname,email,phoneNumber,password,role)
        if(!fullname || !email || !phoneNumber || !password || !role){
            return res.status(400).json({
                message:"Something is missing",
                success:false
            });
        };
        const file = req.file;
        // const fileUri = getDataUri(file);
        // const cloudResponse = await cloudinary.uploader.upload(fileUri.content);
        // const file = req.file;
        // cloudinary ayega idhar
        let cloudResponse
        if(file){
            const fileUri = getDataUri(file);
            cloudResponse = await cloudinary.uploader.upload(fileUri.content);
        }
        const user = await User.findOne({email});
        if(user){
            return res.status(400).json({
                message:"Email already exists",
                success:false
            })
        }
        const hashedPassword = await bcrypt.hash(password, 10);

        await User.create({
            fullname,
            email,
            phoneNumber,
            password:hashedPassword,
            role,
            profile:{
                profilePhoto:cloudResponse.secure_url,
            }
        });

        return res.status(201).json({
            message:"Account created successfully.",
            success:true
        })
    }
    catch(error){
        console.log(error)
    }
}


export const login = async (req, res) => {
    try{
        const {email, password, role} = req.body;
        if(!email|| !password || !role){
            return res.status(400).json({
                message:"Something is missing",
                success:false
            });
        };
        let user = await User.findOne({email});
        if(!user){
            return res.status(400).json({
                message:"Email not found",
                success:false
            })
        };
        const isPasswordMatch = await bcrypt.compare(password, user.password);
        if(!isPasswordMatch){
            return res.status(400).json({
                message:"Invalid password",
                success:false
            })
        };
        // check role if valid or not
        if(role !== user.role){
            return res.status(400).json({
                message:"Account doen't exist with current roles",
                success:false
            })
        };

        const tokenData = {
            userId:user._id
        }
        const token = await jwt.sign(tokenData, process.env.SECRET_KEY, {expiresIn:'1d'});

        user = {
            _id:user._id,
            fullname:user.fullname,
            email:user.email,
            phoneNumber:user.phoneNumber,
            role:user.role,
            profile:user.profile
        }

        return res.status(200).cookie("token", token, {maxAge:1*24*60*60*1000, httpOnly:true, sameSite:'strict'}).json({
            message: `Welcome back ${user.fullname}`,
            user,
            success:true
        })
    }
    catch(error){
        console.log(error)
    }
}


export const logout = async (req, res) => {
    try {
        return res.status(200).cookie("token", "", {maxAge:0}).json({
            message: "Logged out successfully",
            success:true
        })
    }
    catch(error){
        console.log(error)
    }
}


export const updateProfile = async (req, res) => {
    try{
        const {fullname, email, phoneNumber, bio, skills} = req.body;
        const file = req.file;
        // cloudinary ayega idhar
        let cloudResponse
        if(file){
            const fileUri = getDataUri(file);
            cloudResponse = await cloudinary.uploader.upload(fileUri.content);
        }

        let skillsArray;
        if(skills){
             skillsArray = skills.split(",");
        }
        const userId = req.id;  // middle authentication
        let user = await User.findById(userId);
        if(!user){
            return res.status(400).json({
                message:"User not found",
                success:false
            })
        };

        console.log("Cloudinary Upload:", cloudResponse);
        // updating data
        if(fullname) user.fullname = fullname;
        if(email) user.email = email;
        if(phoneNumber) user.phoneNumber = phoneNumber;
        if(bio) user.profile.bio = bio;
        if(skills) user.profile.skills = skillsArray;

        // resume comes later here...
        if(cloudResponse){
            user.profile.resume = cloudResponse.secure_url // save the cloudinary url
            user.profile.resumeOriginalName = file.originalname // Save the original file name
        }
        await user.save()

        user = {
            _id:user._id,
            fullname:user.fullname,
            email:user.email,
            phoneNumber:user.phoneNumber,
            role:user.role,
            profile:user.profile
        }

        return res.status(200).json({
            message:"Profile Updated Successfully",
            user,
            success:true
        })
    }
    catch(error){
        console.log(error)
    }
}