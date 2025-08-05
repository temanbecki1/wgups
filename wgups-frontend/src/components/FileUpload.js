import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Button,
  Box,
  Alert,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  LinearProgress
} from '@mui/material';
import { CloudUpload, Description, CheckCircle, Error } from '@mui/icons-material';

const FileUpload = () => {
  const [files, setFiles] = useState({
    packages: null,
    distances: null,
    addresses: null
  });
  const [uploadStatus, setUploadStatus] = useState({});
  const [uploading, setUploading] = useState(false);

  const fileTypes = [
    { key: 'packages', label: 'Package Data (WGUPS_Package_File.csv)', accept: '.csv' },
    { key: 'distances', label: 'Distance Table (WGUPS_Distance_Table.csv)', accept: '.csv' },
    { key: 'addresses', label: 'Address Data (WGUPS_Address_File.csv)', accept: '.csv' }
  ];

  const handleFileSelect = (fileType, event) => {
    const file = event.target.files[0];
    if (file && file.type === 'text/csv') {
      setFiles(prev => ({
        ...prev,
        [fileType]: file
      }));
      setUploadStatus(prev => ({
        ...prev,
        [fileType]: 'selected'
      }));
    } else {
      setUploadStatus(prev => ({
        ...prev,
        [fileType]: 'error'
      }));
    }
  };

  const handleUpload = async () => {
    setUploading(true);
    
    // Simulate file upload process
    const fileKeys = Object.keys(files);
    for (let i = 0; i < fileKeys.length; i++) {
      const key = fileKeys[i];
      if (files[key]) {
        setUploadStatus(prev => ({
          ...prev,
          [key]: 'uploading'
        }));
        
        // Simulate upload delay
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        setUploadStatus(prev => ({
          ...prev,
          [key]: 'success'
        }));
      }
    }
    
    setUploading(false);
    
    // In a real implementation, you would:
    // 1. Upload files to the server
    // 2. Trigger reinitialization of the routing algorithm
    // 3. Update the UI to reflect new data
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'selected':
      case 'success':
        return <CheckCircle color="success" />;
      case 'uploading':
        return <LinearProgress sx={{ width: '100px' }} />;
      case 'error':
        return <Error color="error" />;
      default:
        return <Description color="disabled" />;
    }
  };

  const getStatusText = (status, fileName) => {
    switch (status) {
      case 'selected':
        return `Selected: ${fileName}`;
      case 'uploading':
        return 'Uploading...';
      case 'success':
        return 'Upload successful';
      case 'error':
        return 'Error: Please select a valid CSV file';
      default:
        return 'No file selected';
    }
  };

  const allFilesSelected = Object.values(files).every(file => file !== null);
  const hasErrors = Object.values(uploadStatus).some(status => status === 'error');

  return (
    <Card>
      <CardContent>
        <Box display="flex" alignItems="center" mb={3}>
          <CloudUpload sx={{ mr: 1, color: 'primary.main' }} />
          <Typography variant="h5" component="h2">
            CSV File Upload
          </Typography>
        </Box>

        <Alert severity="info" sx={{ mb: 3 }}>
          Upload your own CSV files to update the routing data. Make sure the files match the expected format.
        </Alert>

        <Paper elevation={1} sx={{ p: 2, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Upload Files
          </Typography>
          
          <List>
            {fileTypes.map((fileType) => (
              <ListItem key={fileType.key} divider>
                <ListItemIcon>
                  {getStatusIcon(uploadStatus[fileType.key])}
                </ListItemIcon>
                <ListItemText
                  primary={fileType.label}
                  secondary={getStatusText(uploadStatus[fileType.key], files[fileType.key]?.name)}
                />
                <input
                  accept={fileType.accept}
                  style={{ display: 'none' }}
                  id={`upload-${fileType.key}`}
                  type="file"
                  onChange={(e) => handleFileSelect(fileType.key, e)}
                />
                <label htmlFor={`upload-${fileType.key}`}>
                  <Button variant="outlined" component="span" size="small">
                    Select File
                  </Button>
                </label>
              </ListItem>
            ))}
          </List>
        </Paper>

        <Box textAlign="center">
          <Button
            variant="contained"
            size="large"
            onClick={handleUpload}
            disabled={!allFilesSelected || hasErrors || uploading}
            startIcon={<CloudUpload />}
          >
            {uploading ? 'Uploading...' : 'Upload and Process Files'}
          </Button>
        </Box>

        {uploading && (
          <Box mt={2}>
            <Typography variant="body2" color="textSecondary" textAlign="center">
              Processing files and updating routing data...
            </Typography>
          </Box>
        )}

        <Alert severity="warning" sx={{ mt: 3 }}>
          <Typography variant="body2">
            <strong>Note:</strong> This is a demo interface. In a production environment, uploading new files would:
            <br />• Validate file formats and data integrity
            <br />• Update the database with new package and route information
            <br />• Reinitialize the routing algorithm with the new data
            <br />• Refresh all displayed information
          </Typography>
        </Alert>
      </CardContent>
    </Card>
  );
};

export default FileUpload; 