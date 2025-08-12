import React, { useEffect, useState } from "react";
import Navbar from "./ui/shared/Navbar";
import FilterCard from "./FilterCard";
import Job from "./Job";
import { useSelector } from "react-redux";
import { motion } from "framer-motion";

// const jobsArray = [1, 2, 3, 4, 5, 6, 7, 8];

const Jobs = () => {
  const {allJobs, searchedQuery} = useSelector(store => store.job)
  const [filteredJobs, setFilteredJobs] = useState(allJobs);

useEffect(() => {
  let filtered = allJobs;

  const salaryRangeRegex = /^\d+\s*-\s*\d+$/;

  if (salaryRangeRegex.test(searchedQuery)) {
    const [min, max] = searchedQuery.split('-').map(Number);
    filtered = filtered.filter(
      job => job.salary >= min && job.salary <= max
    );
  } else if (searchedQuery) {
    const q = searchedQuery.toLowerCase();
    filtered = filtered.filter(
      job =>
        job.title.toLowerCase().includes(q)       ||
        job.description.toLowerCase().includes(q) ||
        job.location.toLowerCase().includes(q)
    );
  }

  setFilteredJobs(filtered);
}, [allJobs, searchedQuery]);


  return (
    <div>
      <Navbar />
      <div className="max-w-7xl mx-auto mt-5">
        <div className="flex gap-5">
          <div className="w-1/4">
            <FilterCard />
          </div>
          <div className="w-3/4 h-[88vh] overflow-y-auto pb-5">
            {filteredJobs.length <= 0 ? (
              <span>Job not found</span>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 my-5">
                {filteredJobs.map((job) => (
                  <motion.div
                  initial={{opacity:0, x:100}}
                  animate={{opacity:1, x:0}}
                  exit={{opacity:0,x:-100}}
                  transition={{duration:0.3}}
                  key={job?._id}>
                  <Job job={job} />
                  </motion.div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};


export default Jobs;