import { useDispatch } from "react-redux";
import { Route, Routes } from "react-router-dom";
import BuyerBot from "./pages/ChatBot";

function App() {
  const dispatch = useDispatch();
 
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
