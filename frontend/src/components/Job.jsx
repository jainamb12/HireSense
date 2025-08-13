import React, { useState } from "react";
import { Button } from "./ui/button";
import { Bookmark } from "lucide-react";
import { Badge } from "./ui/badge";
import { Avatar, AvatarImage } from "./ui/avatar";
import { useNavigate } from "react-router-dom";
import { useAnalyzeResume } from "../hooks/useAnalyzeResume";
import { useSelector } from 'react-redux'; 


const Job = ({job}) => {
  const navigate = useNavigate();
  const { user } = useSelector(store => store.auth);
  
  const [showAnalysis, setShowAnalysis] = useState(false);
  const { data, loading, error, analyzeResume } = useAnalyzeResume();

  const daysAgoFunction = (mongodbTime) => {
    const createdAt = new Date(mongodbTime);
    const now = new Date();
    const timeDifference = now - createdAt;
    return Math.floor(timeDifference / (1000 * 60 * 60 * 24));
  };

  const handleAnalyzeClick = () => {
    const resumeUrl = user?.profile?.resume;
    if (resumeUrl) {
      // Assuming 'job.description' is the full text of the job description
      analyzeResume(resumeUrl, job.description);
      setShowAnalysis(true);
    } else {
      alert("Please upload your resume to your profile first.");
    }
  };

  return (
    <div className="p-5 rounded-md shadow-xl bg-white border-gray-100">
      <div className="flex items-center justify-between">
        <p className="text-sm text-gray-500">{daysAgoFunction(job?.createdAt) === 0 ? "Today" : `${daysAgoFunction(job?.createdAt)} days ago`}</p>
        <Button variant="outline" className="rounded-full" size="icon">
          <Bookmark />
        </Button>
      </div>
      <div className="flex items-center gap-2 my-2">
        <Button className="p-0 rounded-full w-16 h-16 overflow-hidden flex items-center justify-center">
          <Avatar className="w-full h-full rounded-full">
            <AvatarImage
              src={job?.company?.logo}
              alt={`${job?.company?.name} Logo`}
              className="w-full h-full object-contain object-center bg-gray-100"
            />
          </Avatar>
        </Button>
        <div>
          <h1 className="font-medium text-lg">{job?.company?.name}</h1>
          <p className="text-sm text-gray-500">India</p>
        </div>
      </div>
      <div>
        <h1 className="font-bold text-lg my-2">{job?.title}</h1>
        <p className="text-sm text-gray-600">
          {job?.description}
        </p>
      </div>
      <div className="flex items-center gap-2 mt-4">
        <Badge className="text-blue-700 font-bold" variant="ghost">
          {job?.position} Positions
        </Badge>
        <Badge className="text-[#F83002] font-bold" variant="ghost">
          {job?.jobType}
        </Badge>
        <Badge className="text-[#7209b7] font-bold" variant="ghost">
           {job?.salary} LPA
        </Badge>
      </div>
      <div className="flex justify-between items-center mt-4">
        <div className="flex-item-center gap-4">
          <Button onClick={() => navigate(`/description/${job?._id || job?.id}`)} className="cursor-pointer" variant="outline">Details</Button>
          <Button onClick={handleAnalyzeClick} disabled={loading} className="text-sm cursor-pointer bg-[#7209b7] text-white">
            {loading ? 'Analyzing...' : 'Analyze My Resume Fit'}
          </Button>
        </div>
      </div>

      {/* Conditional rendering for the analysis report */}
      {showAnalysis && (
        <div className="mt-4 p-4 border rounded-md">
          <h3 className="text-xl font-bold mb-2">Analysis Report</h3>
          {loading && <p className="text-gray-700">Analyzing your resume...</p>}
          {error && <p className="text-red-500">Error: {error}</p>}
          {data && (
            <div>
              <p className="text-lg">Overall Match Score: <span className="font-semibold">{data.overall_match_score}%</span></p>

              {/* Matching Skills */}
              <h4 className="font-semibold mt-4">Matching Skills:</h4>
              <ul className="list-disc ml-6">
                {data.matching_skills.map(skill => (
                  <li key={skill} className="text-green-600 font-medium">{skill}</li>
                ))}
              </ul>

              {/* Missing Skills */}
              <h4 className="font-semibold mt-4">Missing Skills:</h4>
              <ul className="list-disc ml-6">
                {data.missing_skills.map(skill => (
                  <li key={skill} className="text-red-600 font-medium">{skill}</li>
                ))}
              </ul>

              {/* Suggestions */}
              <h4 className="font-semibold mt-4">Actionable Suggestions:</h4>
              <ul className="list-disc ml-6 text-gray-700">
                {data.actionable_suggestions.map((s, index) => (
                  <li key={index}>{s}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};


export default Job;