import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Grid,
  Box,
  Paper,
  Chip,
  Alert
} from '@mui/material';
import { Search, Inventory } from '@mui/icons-material';
import axios from 'axios';

const PackageTracker = () => {
  const [packageId, setPackageId] = useState('');
  const [queryTime, setQueryTime] = useState('');
  const [packageData, setPackageData] = useState(null);
  const [statusData, setStatusData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    if (!packageId || !queryTime) {
      setError('Please enter both package ID and time');
      return;
    }

    if (packageId < 1 || packageId > 40) {
      setError('Package ID must be between 1 and 40');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      // Fetch package details
      const packageResponse = await axios.get(`http://localhost:5000/api/package/${packageId}`);
      setPackageData(packageResponse.data);

      // Fetch status at specific time
      const statusResponse = await axios.get(
        `http://localhost:5000/api/package/${packageId}/status?time=${queryTime}`
      );
      setStatusData(statusResponse.data);

    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch package data');
      setPackageData(null);
      setStatusData(null);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    if (!status) return 'default';
    if (status === 'At the hub') return 'default';
    if (status === 'En route') return 'warning';
    if (status === 'Delayed on flight') return 'error';
    if (status.includes('Delivered')) return 'success';
    return 'default';
  };

  return (
    <Card>
      <CardContent>
        <Box display="flex" alignItems="center" mb={3}>
          <Inventory sx={{ mr: 1, color: 'primary.main' }} />
          <Typography variant="h5" component="h2">
            Package Tracker
          </Typography>
        </Box>

        <Grid container spacing={2} mb={3}>
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Package ID"
              type="number"
              value={packageId}
              onChange={(e) => setPackageId(e.target.value)}
              inputProps={{ min: 1, max: 40 }}
              helperText="Enter package ID (1-40)"
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Query Time"
              type="time"
              value={queryTime}
              onChange={(e) => setQueryTime(e.target.value)}
              helperText="Select time to check status"
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <Button
              fullWidth
              variant="contained"
              onClick={handleSearch}
              disabled={loading}
              startIcon={<Search />}
              sx={{ height: '56px' }}
            >
              {loading ? 'Searching...' : 'Track Package'}
            </Button>
          </Grid>
        </Grid>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {packageData && statusData && (
          <Paper elevation={2} sx={{ p: 3 }}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom color="primary">
                  Package Details
                </Typography>
                <Box mb={1}>
                  <Typography variant="body2" color="textSecondary">Package ID</Typography>
                  <Typography variant="body1" fontWeight="bold">#{packageData.id}</Typography>
                </Box>
                <Box mb={1}>
                  <Typography variant="body2" color="textSecondary">Delivery Address (at query time)</Typography>
                  <Typography variant="body1">{statusData.delivery_address}</Typography>
                </Box>
                <Box mb={1}>
                  <Typography variant="body2" color="textSecondary">City</Typography>
                  <Typography variant="body1">{packageData.city}</Typography>
                </Box>
                <Box mb={1}>
                  <Typography variant="body2" color="textSecondary">ZIP Code</Typography>
                  <Typography variant="body1">{packageData.zip}</Typography>
                </Box>
                <Box mb={1}>
                  <Typography variant="body2" color="textSecondary">Weight</Typography>
                  <Typography variant="body1">{packageData.weight} kg</Typography>
                </Box>
                <Box mb={1}>
                  <Typography variant="body2" color="textSecondary">Delivery Deadline</Typography>
                  <Typography variant="body1">{statusData.delivery_deadline}</Typography>
                </Box>
                <Box mb={1}>
                  <Typography variant="body2" color="textSecondary">Truck Number</Typography>
                  <Typography variant="body1">Truck {statusData.truck_number}</Typography>
                </Box>
              </Grid>

              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom color="primary">
                  Status at {queryTime}
                </Typography>
                <Box mb={2}>
                  <Chip
                    label={statusData.delivery_status}
                    color={getStatusColor(statusData.delivery_status)}
                    size="large"
                    sx={{ fontSize: '1rem', p: 1 }}
                  />
                </Box>
                {statusData.delivery_time && (
                  <Box mb={1}>
                    <Typography variant="body2" color="textSecondary">Delivery Time</Typography>
                    <Typography variant="body1">{statusData.delivery_time}</Typography>
                  </Box>
                )}
              </Grid>
            </Grid>
          </Paper>
        )}
      </CardContent>
    </Card>
  );
};

export default PackageTracker; 