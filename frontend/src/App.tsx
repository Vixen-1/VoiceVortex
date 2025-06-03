import { useDispatch } from "react-redux";
import { useEffect } from "react";
import { setDataId } from "./redux/chatbot";
import { Route, Routes } from "react-router-dom";
import BuyerBot from "./pages/ChatBot";

function App() {
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(setDataId("buyer"));
  }, []);
  return (
    <Routes>
      <Route
        path="/"
        element={
            <BuyerBot />
        }
      />
    </Routes>
  );
}

export default App;
