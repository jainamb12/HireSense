import axios from "axios";

export const useHello = () => {
  const getMessage = async () => {
    const { data } = await axios.get("http://localhost:8888/api/ai/hello");
    return data.message;
  };
  return { getMessage };
};
