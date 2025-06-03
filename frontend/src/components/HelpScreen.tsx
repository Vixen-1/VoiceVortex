import { ChevronRight, Search } from "@mui/icons-material";
import {
  Box,
  IconButton,
  OutlinedInput,
  Stack,
  Typography,
} from "@mui/material";
import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { RootState } from "../redux/store";
import { api } from "../services/api";
import { useDispatch } from "react-redux";
import { setActiveTab, setDisplayChat, setNewMessage } from "../redux/chatbot";
import Loader from "../common/Loader";

const InfoScreen = () => {
  const dispatch = useDispatch();
  const [searchValue, setSearchValue] = useState("");
  const [searchError, setSearchError] = useState(
    "Please enter something to search..."
  );
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const dataId = useSelector((state: RootState) => state.chatbot.dataId);
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchValue(e.target.value.toLowerCase());
  };

  const handleSendClick = (message: string = searchValue) => {
    if (message.trim().length === 0) {
      setSearchError("Please enter a message");
    } else {
      dispatch(setDisplayChat(true));
      setSearchError("");
      dispatch(setNewMessage(message));
      setSearchValue("");
      dispatch(setActiveTab("message"));
    }
  };

  const handleSearch = async () => {
    const message = searchValue;
    if (message.trim().length === 0) return;
    setLoading(true);
    const payload = { question: message };
    const url = `/search/`;
    // setSearchValue("");
    try {
      const response = await api.post(url, payload, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (response.data.matching_questions.length === 0)
        setSearchError("No matching questions found");
      else setSearchError("");
      setQuestions(response.data.matching_questions);
    } catch (err) {
      console.error("Error sending message:", err);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setSearchValue("");
    setSearchError("Please enter something to search...");
    setQuestions([]);
  };
  // const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
  //   if (e.key === "Enter" && searchValue.trim().length > 0) {
  //     handleSearch();
  //   }
  // };

  useEffect(() => {
    const timeOutID = setTimeout(async () => {
      if (searchValue.trim()) {
        await handleSearch();
      } else {
        reset();
      }
    }, 500);
    return () => clearTimeout(timeOutID);
  }, [searchValue]);

  return (
    <Stack direction="column" sx={{ position: "relative" }}>
      <Box className="top-headers">
        <Typography
          textAlign={"center"}
          fontWeight="600"
          fontFamily="Poppins"
          sx={{ cursor: "default" }}
        >
          Help
        </Typography>
        <OutlinedInput
          size="small"
          fullWidth
          placeholder="Search..."
          value={searchValue}
          endAdornment={<Search color="disabled" />}
          className="tab-search"
          onChange={handleChange}
          // onKeyDown={handleKeyDown}
        />
      </Box>
      <Box mt={10}>
        {loading ? (
          <Box display={"flex"} justifyContent={"center"}>
            <Loader />
          </Box>
        ) : questions && questions.length > 0 ? (
   
            <Box className="container-column" mb={6}>
              <Typography className="container-text">{`${questions.length || 0} Questions Found`}</Typography>
              {questions.map((question, qIndex) => (
                <Box
                  display={"flex"}
                  flexDirection={"row"}
                  // boxShadow={1}
                  justifyContent={"space-between"}
                  alignItems={"center"}
                  mt={0.5}
                  key={`ambiguous-${qIndex}`}
                  sx={{
                    borderBottom: "0.25px solid #9C9C9C",
                    // borderBottom: '0.25px solid #9C9C9C',
                    boxShadow:
                      "3.31px 1.97px 12px 0px #1C57EE14, -1.66px -1.66px 1.57px 0px #1C57EE14",
                    borderRadius: "3px",
                    paddingX: "8px",
                    cursor: "pointer",
                    "&:hover": {
                      backgroundColor: "#f0f0f0",
                    },
                  }}
                  onClick={() => handleSendClick(question)}
                >
                  <Typography
                    fontFamily="Poppins"
                    fontSize={10}
                    fontWeight={500}
                    color="#000"
                  >
                    {question}
                  </Typography>
                  <IconButton>
                    <ChevronRight
                      sx={{ height: "15px", width: "15px", color: "black" }}
                    />
                  </IconButton>
                </Box>
              ))}
            </Box>
        ) : (
          <Box mt={5}>
            <Typography
              color="#757575"
              fontFamily="Poppins"
              fontSize={12}
              textAlign="center"
            >
              {searchError}
            </Typography>
          </Box>
        )}
      </Box>
    </Stack>
  );
};

export default InfoScreen;
