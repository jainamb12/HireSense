import React, { useEffect, useState } from 'react'
import { RadioGroup, RadioGroupItem } from './ui/radio-group'
import { Label } from './ui/label'
import { useDispatch } from 'react-redux';
import { setSearchedQuery } from '@/redux/jobSlice'
const filterData = [
  {
    filterType:"Location",
    array:["Ahmedabad", "Pune", "Mumbai", "Bangalore", "Chennai", "Hyderabad", "Delhi NCR"]
  },
  {
    filterType:"Industry",
    array:["Frontend Developer", "Backend Developer", "FullStack Developer"]
  },
  {
    filterType:"Salary (LPA)",
    // array:["0-40k","40k-100k", "100k-500k"]
    array:["0-4","4-10","10-50"]
  },
]

function FilterCard() {
  const [selectedValue, setSelectedValue] = useState('');
  const dispatch = useDispatch();

  const changeHandler = (value) => {
    setSelectedValue(value);
  }

  useEffect(() => {
   dispatch(setSearchedQuery(selectedValue))
  },[selectedValue, dispatch])

  return (
    <div className='w-full bg-white p-3 rounded-md'>
      <h1 className='font-bold text-2xl'>Filter Jobs</h1>
      <hr className='mt-3'/>
      <RadioGroup value={selectedValue}  onValueChange={changeHandler}>
        {
          filterData.map((data, index) => (
            <div key={index} className='mb-6'>
              <h1 className='font-bold text-lg'>
                {data.filterType}
              </h1>
              {
                data.array.map((item, idx) => {
                  const itemId = `id${index}-${idx}`
                  return (
                    <div key={idx} className="flex items-center space-x-2 mb-2">
                      <RadioGroupItem value={item} id={itemId}/>
                      <Label className="text-gray-600" htmlFor={itemId}>{item}</Label>
                    </div>
                  )
                })
              }
            </div>
          ))
        }
      </RadioGroup>
    </div>
  )
}

export default FilterCard
