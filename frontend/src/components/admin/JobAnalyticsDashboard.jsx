// components/admin/JobAnalyticsDashboard.jsx

import React, { useState } from 'react';
import Navbar from '../ui/shared/Navbar';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card.jsx';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select.jsx';
import { Bar, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import { useJobAnalytics } from '../../hooks/useJobAnalytics';

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

const JobAnalyticsDashboard = () => {
  const [selectedLocation, setSelectedLocation] = useState('all');
  const [selectedJobType, setSelectedJobType] = useState('all');
  const { data, loading, error } = useJobAnalytics(selectedLocation, selectedJobType);

  const topSkillsData = data?.top_skills ? {
    labels: data.top_skills.map(item => item.skill),
    datasets: [{
      label: 'Frequency',
      data: data.top_skills.map(item => item.count),
      backgroundColor: 'rgba(106, 56, 194, 0.6)',
      borderColor: 'rgba(106, 56, 194, 1)',
      borderWidth: 1,
    }],
  } : null;

  const jobTypeData = data?.job_type_distribution ? {
    labels: data.job_type_distribution.map(item => item.job_type),
    datasets: [{
      label: 'Job Distribution',
      data: data.job_type_distribution.map(item => item.count),
      backgroundColor: ['rgba(75, 192, 192, 0.6)', 'rgba(255, 99, 132, 0.6)', 'rgba(54, 162, 235, 0.6)'],
      borderColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)'],
      borderWidth: 1,
    }],
  } : null;

  const averageSalaryData = data?.avg_salary_by_location ? {
    labels: data.avg_salary_by_location.map(item => item.location),
    datasets: [{
      label: 'Average Salary (LPA)',
      data: data.avg_salary_by_location.map(item => item.avg_salary),
      backgroundColor: 'rgba(248, 48, 2, 0.6)',
      borderColor: 'rgba(248, 48, 2, 1)',
      borderWidth: 1,
    }],
  } : null;

  const uniqueLocations = data?.unique_locations || [];
  const uniqueJobTypes = data?.unique_job_types || [];

  return (
    <div>
      <Navbar />
      <div className="max-w-7xl mx-auto my-8 p-6">
        <h1 className="text-3xl font-bold mb-6">Job Market Analytics Dashboard</h1>
        
        {/* Filter Section */}
        <div className="flex gap-4 mb-8">
          <div className="flex items-center gap-2">
            <label>Location:</label>
            <Select onValueChange={setSelectedLocation} value={selectedLocation}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Select Location" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Locations</SelectItem>
                {uniqueLocations.map(loc => <SelectItem key={loc} value={loc}>{loc}</SelectItem>)}
              </SelectContent>
            </Select>
          </div>

          <div className="flex items-center gap-2">
            <label>Job Type:</label>
            <Select onValueChange={setSelectedJobType} value={selectedJobType}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Select Job Type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Job Types</SelectItem>
                {uniqueJobTypes.map(type => <SelectItem key={type} value={type}>{type}</SelectItem>)}
              </SelectContent>
            </Select>
          </div>
        </div>

        {loading && <div className="text-center text-gray-500">Loading data...</div>}
        {error && <div className="text-center text-red-500">{error}</div>}
        {!loading && !error && data && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Top In-Demand Skills Chart */}
            <Card>
              <CardHeader>
                <CardTitle>Top 10 In-Demand Skills</CardTitle>
              </CardHeader>
              <CardContent>
                {topSkillsData?.labels.length > 0 ? <Bar data={topSkillsData} /> : <p className="text-gray-500">No data available.</p>}
              </CardContent>
            </Card>

            {/* Job Type Distribution Chart */}
            <Card>
              <CardHeader>
                <CardTitle>Job Type Distribution</CardTitle>
              </CardHeader>
              <CardContent className="h-64 flex items-center justify-center">
                {jobTypeData?.labels.length > 0 ? <Pie data={jobTypeData} /> : <p className="text-gray-500">No data available.</p>}
              </CardContent>
            </Card>

            {/* Average Salary by Location Chart */}
            <Card>
              <CardHeader>
                <CardTitle>Average Salary by Location</CardTitle>
              </CardHeader>
              <CardContent>
                {averageSalaryData?.labels.length > 0 ? <Bar data={averageSalaryData} /> : <p className="text-gray-500">No data available.</p>}
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
};

export default JobAnalyticsDashboard;