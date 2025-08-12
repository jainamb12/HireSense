import { useMatchedJobs } from "../hooks/useMatchedJobs";
import JobCard from "./Job.jsx";
import { Badge } from "./ui/badge.jsx"; // Assuming this is your custom Badge component

const RecommendedJobs = () => {
  const { matches, loading, error } = useMatchedJobs();

  if (loading) {
    return (
      <div className='max-w-7xl mx-auto my-20'>
        <p className="p-4 text-gray-700">Finding the best jobs for you…</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className='max-w-7xl mx-auto my-20'>
        <p className="p-4 text-red-600">Error fetching recommendations: {error}</p>
      </div>
    );
  }

  // Display a message if no matches are found
  if (!matches || matches.length === 0) {
    return (
      <section className="max-w-7xl mx-auto my-20">
        <h2 className="text-4xl font-bold mb-4">
          <span className='text-[#6A38C2]'>Recommended </span>Job Openings
        </h2>
        <p className="p-4 text-gray-600">No job recommendations available at the moment. Please update your profile or check back later!</p>
      </section>
    );
  }

  return (
    <section className="max-w-7xl mx-auto my-20">
      <h2 className="text-4xl font-bold mb-4">
        <span className='text-[#6A38C2]'>Recommended </span>Job Openings
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 my-5">
        {matches.slice(0, 6).map(job => (
          <div key={job._id} className="group relative border rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200 p-4"> {/* Added padding directly to this div */}
            {/* The JobCard component will be rendered here */}
            <JobCard job={job} />

            {/* Score Display Area - Now below the JobCard content */}
            <div className="mt-4 pt-2 border-t border-gray-200 flex justify-between items-center text-sm font-semibold">
                {/* Skill Match - Left aligned */}
                <div className="flex items-center space-x-1">
                    <span className="text-gray-600">Skill Match:</span>
                    <span className={
                        job.skill_coverage >= 80 ? "text-green-600"
                        : job.skill_coverage >= 50 ? "text-yellow-600"
                        : "text-gray-500" // Use a more neutral color for lower matches if not using red
                    }>
                        {job.skill_coverage.toFixed(0)}%
                    </span>
                </div>

                {/* Relevance (Cosine) - Right aligned */}
                <div className="flex items-center space-x-1">
                    <span className="text-gray-600">Relevance:</span>
                    <span className="text-gray-500 italic"> {/* Keep relevance more subdued */}
                        {job.cosine_score.toFixed(1)}%
                    </span>
                </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default RecommendedJobs;