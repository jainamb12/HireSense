import { useEffect, useState } from "react";
import { useHello } from "../hooks/useHello";

const Hello = () => {
  const { getMessage } = useHello();
  const [message, setMessage] = useState("");

  useEffect(() => {
    // Call the Python API via backend when the component mounts
    getMessage().then(setMessage);
  }, []);

  return (
    <div className="p-4 text-xl text-green-600">
      Python says: {message}
    </div>
  );
};

export default Hello;