import { ChevronRight, Search } from "@mui/icons-material";
import {
  Box,
  IconButton,
  OutlinedInput,
  Stack,
  Typography,
} from "@mui/material";
import React, { useState } from "react";

const InfoScreen = () => {
  const [searchValue, setSearchValue] = useState("");
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchValue(e.target.value.toLowerCase());
  };
  return (
    <Stack direction="column" height="100vh" sx={{ position: "relative" }}>
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
          sx={{ ml: 8, my: 0.5 }}
          size="small"
          placeholder="Search"
          value={searchValue}
          endAdornment={<Search color="disabled" />}
          className="tab-search"
          onChange={handleChange}
        />
      </Box>
      <Box className="container-blocks" mt={12} marginX={2}>
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

export default InfoScreen;
