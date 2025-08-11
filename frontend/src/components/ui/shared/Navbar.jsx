import { Link, useNavigate } from "react-router-dom";
import React from "react";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { LogOutIcon, User2 } from "lucide-react";
import { useDispatch, useSelector } from "react-redux";
import { USER_API_END_POINT } from "../../../utils/constant";
import { setUser } from "../../../redux/authSlice";
import { toast } from "sonner";
import axios from "axios";


const Navbar = () => {
  const {user} = useSelector(store => store.auth);
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const logoutHandler = async () => {
    try{
      const res = await axios.get(`${USER_API_END_POINT}/logout`, {withCredentials:true})
      if(res.data.success){
        dispatch(setUser(null));
        navigate("/")
        toast.success(res.data.message)
      }
    }
    catch(error){
      console.log(error)
      toast.error(error.response.data.message)
    }
  }
  return (
    <div className="bg-white">
      <div className="flex item-center justify-between mx-auto max-w-7xl h-16">
        <div>
          <h1 className="text-3xl my-3 font-bold">
            Hire<span className="text-[#F83002]">Sense</span>
          </h1>
        </div>
        <div className="flex items-center gap-12">
          <ul className="flex font-medium items-center gap-5">
            {
              user && user.role === "recruiter" ? (
                <>
                  <li><Link to="/admin/companies">Companies</Link></li>
                  <li><Link to="/admin/jobs">Jobs</Link></li>
                  <li><Link to="/admin/analytics">Analytics</Link></li>
                </>
              ) : (
                <>
                  <li><Link to="/">Home</Link></li>
                  <li><Link to="/jobs">Jobs</Link></li>
                  <li><Link to="/browse">Browse</Link></li>
                  <li><Link to="/analytics">Analytics</Link></li>
                </>
              )
            }
          </ul>
          {!user ? (
            <div className="flex item-center gap-2">
                <Link to="/login"><Button className="cursor-pointer" variant="outline">Login</Button></Link>
                <Link to="/signup"><Button className="cursor-pointer bg-[#6A38C2] hover: bg-[#5b30a6]">Signup</Button></Link>
            </div>
          ) : (
            <Popover>
              <PopoverTrigger asChild>
                <Avatar className="cursor-pointer">
                  <AvatarImage
                    src={user?.profile?.profilePhoto}
                    alt="@shadcn"
                  />
                </Avatar>
              </PopoverTrigger>
              <PopoverContent className="w-80">
                <div className="">
                  <Avatar className="cursor-pointer">
                    <AvatarImage
                      src={user?.profile?.profilePhoto}
                      alt="@shadcn"
                    />
                  </Avatar>
                  <div>
                    <h4 className="font-medium">{user?.fullname}</h4>
                    <p className="text-sm text-muted-foreground">
                      {user?.profile?.bio}
                    </p>
                  </div>
                </div>

                <div className="flex flex-col my-2 text-gray-600">
                  {
                    user && user.role === "student" && (
                      <>
                         <div className="flex w-fit items-center gap-2 cursor-pointer">
                          <User2 />
                          <Button variant="link"><Link to="/profile">View Profile</Link></Button>
                         </div>
                      </>
                    )
                  }
                  <div className="flex w-fit items-center gap-2 cursor-pointer">
                    <LogOutIcon />
                    <Button onClick={logoutHandler} variant="link">Logout</Button>
                  </div>
                </div>
              </PopoverContent>
            </Popover>
          )}
        </div>
      </div>
    </div>
  );
};

export default Navbar;