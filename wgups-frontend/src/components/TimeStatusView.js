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
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from '@mui/material';
import { Timeline, ExpandMore, LocalShipping } from '@mui/icons-material';
import axios from 'axios';

const TimeStatusView = () => {
  const [queryTime, setQueryTime] = useState('');
  const [packagesData, setPackagesData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Preset times for required screenshots
  const presetTimes = [
    { label: 'Between 8:35-9:25 AM', time: '09:00' },
    { label: 'Between 9:35-10:25 AM', time: '10:00' },
    { label: 'Between 12:03-1:12 PM', time: '12:30' }
  ];

  const handleSearch = async (time = queryTime) => {
    if (!time) {
      setError('Please select a time');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await axios.get(`http://localhost:5000/api/packages/status?time=${time}`);
      setPackagesData(response.data);
      setQueryTime(time);

    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch packages data');
      setPackagesData(null);
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

  const groupPackagesByTruck = (packages) => {
    const grouped = { 1: [], 2: [], 3: [] };
    packages.forEach(pkg => {
      if (pkg.truck_number && grouped[pkg.truck_number]) {
        grouped[pkg.truck_number].push(pkg);
      }
    });
    return grouped;
  };

  const formatTime = (time) => {
    const [hour, minute] = time.split(':');
    const hourInt = parseInt(hour);
    const ampm = hourInt >= 12 ? 'PM' : 'AM';
    const displayHour = hourInt === 0 ? 12 : hourInt > 12 ? hourInt - 12 : hourInt;
    return `${displayHour}:${minute} ${ampm}`;
  };

  return (
    <Card>
      <CardContent>
        <Box display="flex" alignItems="center" mb={3}>
          <Timeline sx={{ mr: 1, color: 'primary.main' }} />
          <Typography variant="h5" component="h2">
            Time Status View - All Packages by Truck
          </Typography>
        </Box>

        <Grid container spacing={2} mb={3}>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Query Time"
              type="time"
              value={queryTime}
              onChange={(e) => setQueryTime(e.target.value)}
              helperText="Select time to view all package statuses"
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <Button
              fullWidth
              variant="contained"
              onClick={() => handleSearch()}
              disabled={loading}
              sx={{ height: '56px' }}
            >
              {loading ? 'Loading...' : 'View Status at Time'}
            </Button>
          </Grid>
        </Grid>

        {/* Preset time buttons for screenshots */}
        <Box mb={3}>
          <Typography variant="h6" gutterBottom>
            Quick Select (Required Screenshot Times):
          </Typography>
          <Grid container spacing={1}>
            {presetTimes.map((preset, index) => (
              <Grid item key={index}>
                <Button
                  variant="outlined"
                  size="small"
                  onClick={() => handleSearch(preset.time)}
                  disabled={loading}
                >
                  {preset.label}
                </Button>
              </Grid>
            ))}
          </Grid>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {packagesData && (
          <Box>
            <Typography variant="h6" gutterBottom color="primary">
              Package Status at {formatTime(packagesData.query_time)}
            </Typography>
            
            {Object.entries(groupPackagesByTruck(packagesData.packages)).map(([truckId, packages]) => (
              <Accordion key={truckId} defaultExpanded sx={{ mb: 2 }}>
                <AccordionSummary
                  expandIcon={<ExpandMore />}
                  aria-controls={`truck${truckId}-content`}
                  id={`truck${truckId}-header`}
                >
                  <Box display="flex" alignItems="center">
                    <LocalShipping sx={{ mr: 1 }} />
                    <Typography variant="h6">
                      Truck {truckId} ({packages.length} packages)
                    </Typography>
                  </Box>
                </AccordionSummary>
                <AccordionDetails>
                  <TableContainer component={Paper} elevation={1}>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell><strong>ID</strong></TableCell>
                          <TableCell><strong>Address</strong></TableCell>
                          <TableCell><strong>City</strong></TableCell>
                          <TableCell><strong>Zip</strong></TableCell>
                          <TableCell><strong>Weight</strong></TableCell>
                          <TableCell><strong>Deadline</strong></TableCell>
                          <TableCell><strong>Status</strong></TableCell>
                          <TableCell><strong>Delivery Time</strong></TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {packages.map((pkg) => (
                          <TableRow key={pkg.id} hover>
                            <TableCell>{pkg.id}</TableCell>
                            <TableCell>{pkg.delivery_address}</TableCell>
                            <TableCell>{pkg.city}</TableCell>
                            <TableCell>{pkg.zip}</TableCell>
                            <TableCell>{pkg.weight} kg</TableCell>
                            <TableCell>{pkg.delivery_deadline}</TableCell>
                            <TableCell>
                              <Chip
                                label={pkg.delivery_status}
                                color={getStatusColor(pkg.delivery_status)}
                                size="small"
                                variant="outlined"
                              />
                            </TableCell>
                            <TableCell>{pkg.delivery_time || 'Not delivered'}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </AccordionDetails>
              </Accordion>
            ))}

            {/* Summary Statistics */}
            <Paper elevation={2} sx={{ p: 2, mt: 2, bgcolor: 'grey.50' }}>
              <Typography variant="h6" gutterBottom>Summary</Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} md={3}>
                  <Typography variant="body2" color="textSecondary">Total Packages</Typography>
                  <Typography variant="h5">{packagesData.packages.length}</Typography>
                </Grid>
                <Grid item xs={12} md={3}>
                  <Typography variant="body2" color="textSecondary">At Hub</Typography>
                  <Typography variant="h5" color="grey.600">
                    {packagesData.packages.filter(p => p.delivery_status === 'At the hub').length}
                  </Typography>
                </Grid>
                <Grid item xs={12} md={3}>
                  <Typography variant="body2" color="textSecondary">En Route / Delayed</Typography>
                  <Typography variant="h5" color="warning.main">
                    {packagesData.packages.filter(p => p.delivery_status === 'En route' || p.delivery_status === 'Delayed on flight').length}
                  </Typography>
                </Grid>
                <Grid item xs={12} md={3}>
                  <Typography variant="body2" color="textSecondary">Delivered</Typography>
                  <Typography variant="h5" color="success.main">
                    {packagesData.packages.filter(p => p.delivery_status && p.delivery_status.includes('Delivered')).length}
                  </Typography>
                </Grid>
              </Grid>
            </Paper>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default TimeStatusView; 