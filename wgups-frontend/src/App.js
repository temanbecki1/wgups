import React, { useState, useEffect } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
  Tab,
  Tabs,
  ThemeProvider,
  createTheme,
  CssBaseline
} from '@mui/material';
import { LocalShipping, Timeline, Upload } from '@mui/icons-material';
import PackageTracker from './components/PackageTracker';
import TimeStatusView from './components/TimeStatusView';
import FileUpload from './components/FileUpload';
import TotalMileage from './components/TotalMileage';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#f50057',
    },
  },
});

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

function App() {
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <LocalShipping sx={{ mr: 2 }} />
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              WGUPS Package Routing System
            </Typography>
            <Typography variant="body2">
              Student ID: 012172824
            </Typography>
          </Toolbar>
        </AppBar>

        <Container maxWidth="lg" sx={{ mt: 2 }}>
          <TotalMileage />
          
          <Box sx={{ borderBottom: 1, borderColor: 'divider', mt: 2 }}>
            <Tabs value={tabValue} onChange={handleTabChange} aria-label="navigation tabs">
              <Tab 
                icon={<LocalShipping />} 
                label="Package Tracker" 
                id="tab-0"
                aria-controls="tabpanel-0"
              />
              <Tab 
                icon={<Timeline />} 
                label="Time Status View" 
                id="tab-1"
                aria-controls="tabpanel-1"
              />
              <Tab 
                icon={<Upload />} 
                label="File Upload" 
                id="tab-2"
                aria-controls="tabpanel-2"
              />
            </Tabs>
          </Box>

          <TabPanel value={tabValue} index={0}>
            <PackageTracker />
          </TabPanel>
          <TabPanel value={tabValue} index={1}>
            <TimeStatusView />
          </TabPanel>
          <TabPanel value={tabValue} index={2}>
            <FileUpload />
          </TabPanel>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App; 