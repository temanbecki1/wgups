import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Grid,
  Box,
  Chip
} from '@mui/material';
import { LocalShipping } from '@mui/icons-material';
import axios from 'axios';

const TotalMileage = () => {
  const [mileageData, setMileageData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchMileageData();
  }, []);

  const fetchMileageData = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://localhost:5000/api/total-mileage');
      setMileageData(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch mileage data');
      console.error('Error fetching mileage:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Typography>Loading mileage data...</Typography>;
  if (error) return <Typography color="error">{error}</Typography>;
  if (!mileageData) return null;

  const isUnder140 = mileageData.total_mileage < 140;

  return (
    <Card elevation={3} sx={{ mb: 2 }}>
      <CardContent>
        <Box display="flex" alignItems="center" mb={2}>
          <LocalShipping sx={{ mr: 1, color: 'primary.main' }} />
          <Typography variant="h5" component="h2">
            Total Mileage Summary
          </Typography>
        </Box>
        
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={6}>
            <Typography variant="h3" component="div" color={isUnder140 ? 'success.main' : 'error.main'}>
              {mileageData.total_mileage.toFixed(2)} miles
            </Typography>
            <Chip 
              label={isUnder140 ? "✓ Under 140 miles" : "⚠ Over 140 miles"} 
              color={isUnder140 ? "success" : "error"}
              variant="outlined"
              sx={{ mt: 1 }}
            />
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Typography variant="h6" gutterBottom>Individual Truck Mileage:</Typography>
            {mileageData.individual_mileage.map(truck => (
              <Box key={truck.truck_id} display="flex" justifyContent="space-between" mb={1}>
                <Typography>Truck {truck.truck_id}:</Typography>
                <Typography fontWeight="bold">{truck.mileage.toFixed(2)} miles</Typography>
              </Box>
            ))}
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default TotalMileage; 