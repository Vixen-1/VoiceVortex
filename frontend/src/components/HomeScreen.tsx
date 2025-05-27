import {
  ChevronRight,
  ScheduleOutlined,
  Search,
  SendOutlined,
} from "@mui/icons-material";
import {
  Box,
  IconButton,
  OutlinedInput,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import React, { useState } from "react";
import chatbot from "../assets/chatbot3.jpg";
import { useDispatch } from "react-redux";
import { setActiveTab, setDisplayChat, setNewMessage } from "../redux/chatbot";
import { useNavigate } from "react-router-dom";

const HomeScreen = () => {
  const dispatch = useDispatch();
  // const navigate = useNavigate();
  const [messageValue, setMessageValue] = useState("");
  const [searchValue, setSearchValue] = useState("");
  const [messageError, setMessageError] = useState("");

  const handleMessageValue = (e: React.ChangeEvent<HTMLInputElement>) => {
    setMessageValue(e.target.value);
    setMessageError("");
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchValue(e.target.value.toLowerCase());
  };

  const handleSendClick = () => {
    if (messageValue.trim().length === 0) {
      setMessageError("Please enter a message");
    } else {
      dispatch(setDisplayChat(true))
      setMessageError("");
      dispatch(setNewMessage(messageValue));
      setMessageValue("");
      dispatch(setActiveTab("message"))
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && messageValue.trim().length > 0) {
      handleSendClick();
    }
  };
  return (
    <Stack
      direction={"column"}
      gap={1.2}
      padding={2}
      justifyContent={"center"}
      alignItems={"flex-start"}
      sx={{ background: "linear-gradient(180deg, #012954, #27517E, #FFFFFF)" }}
    >
      <img src={chatbot} alt="Chatbot" className="chatbot-image" />
      <Box
        display="flex"
        flexDirection="column"
        justifyContent="flex-start"
        alignItems="flex-start"
      >
        <Typography className="header-style">Welcome to Chatbot!</Typography>
        <Typography className="header-style">How can I help?</Typography>
      </Box>
      <Box className="container">
        <Typography className="container-text">
          Schedule call with our product expert
        </Typography>
        <IconButton className="document-icon">
          <ScheduleOutlined />
        </IconButton>
      </Box>
      <Box className="container">
        <TextField
          className="creation-fields"
          fullWidth
          value={messageValue}
          placeholder="Send us a message"
          onChange={handleMessageValue}
          onKeyDown={handleKeyDown}
        />
        <IconButton
          disabled={messageValue.trim().length === 0}
          className="document-icon"
          onClick={handleSendClick}
          area-label="send message"
        >
          <SendOutlined />
        </IconButton>
      </Box>
      {messageError && (
        <Typography color="error" fontSize="9px" ml={3}>
          {messageError}
        </Typography>
      )}
      <Box className="container-blocks">
        <OutlinedInput
          size="small"
          placeholder="Search"
          value={searchValue}
          endAdornment={<Search color="disabled" />}
          className="tab-search"
          onChange={handleChange}
        />
        <Box
          display="flex"
          flexDirection="row"
          justifyContent="space-between"
          alignItems="center"
        >
          <Typography className="container-text">
            Location Section Overview
          </Typography>
          <IconButton>
            <ChevronRight />
          </IconButton>
        </Box>
        <Box
          display="flex"
          flexDirection="row"
          justifyContent="space-between"
          alignItems="center"
        >
          <Typography className="container-text">
            How to Add, Edit, or Remove users
          </Typography>
          <IconButton>
            <ChevronRight />
          </IconButton>
        </Box>
        <Box
          display="flex"
          flexDirection="row"
          justifyContent="space-between"
          alignItems="center"
        >
          <Typography className="container-text">
            How to create meter work order triggers
          </Typography>
          <IconButton>
            <ChevronRight />
          </IconButton>
        </Box>
        <Box
          display="flex"
          flexDirection="row"
          justifyContent="space-between"
          alignItems="center"
        >
          <Typography className="container-text">
            How to create PM schedules
          </Typography>
          <IconButton>
            <ChevronRight />
          </IconButton>
        </Box>
      </Box>
    </Stack>
  );
};

export default HomeScreen;
