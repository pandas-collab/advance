import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Avatar,
  Chip,
  Alert
} from '@mui/material';
import { Person, Calculate, Timeline } from '@mui/icons-material';
import { getCalculationHistory, getUserProfile } from '../../services/api';
import { ICalculation, IUser } from '../../types/api';

export const Dashboard: React.FC = () => {
  const [user, setUser] = useState<IUser | null>(null);
  const [calculations, setCalculations] = useState<ICalculation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [userProfile, calculationHistory] = await Promise.all([
        getUserProfile(),
        getCalculationHistory()
      ]);
      setUser(userProfile);
      setCalculations(calculationHistory);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const exportCalculations = () => {
    const csvContent = [
      'Birth Date,Target Date,Years,Months,Days,Total Days,Created At',
      ...calculations.map(calc =>
        `${calc.birth_date},${calc.target_date},${calc.years},${calc.months},${calc.days},${calc.total_days},${calc.created_at}`
      )
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'age_calculations.csv';
    a.click();
    window.URL.revokeObjectURL(url);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <Typography>Loading dashboard...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        User Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* User Profile Section */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Avatar sx={{ mr: 2, bgcolor: 'primary.main' }}>
                  <Person />
                </Avatar>
                <Box>
                  <Typography variant="h6">{user?.full_name}</Typography>
                  <Typography variant="body2" color="textSecondary">
                    {user?.email}
                  </Typography>
                </Box>
              </Box>
              <Chip
                label={user?.is_admin ? 'Admin User' : 'Standard User'}
                color={user?.is_admin ? 'secondary' : 'primary'}
                size="small"
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Analytics Cards */}
        <Grid item xs={12} md={8}>
          <Grid container spacing={2}>
            <Grid item xs={6} md={4}>
              <Card>
                <CardContent>
                  <Box display="flex" alignItems="center">
                    <Calculate sx={{ mr: 1, color: 'primary.main' }} />
                    <Box>
                      <Typography variant="h5">{calculations.length}</Typography>
                      <Typography variant="body2">Total Calculations</Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={6} md={4}>
              <Card>
                <CardContent>
                  <Box display="flex" alignItems="center">
                    <Timeline sx={{ mr: 1, color: 'secondary.main' }} />
                    <Box>
                      <Typography variant="h5">
                        {calculations.length > 0 ?
                          Math.round(calculations.reduce((sum, calc) => sum + calc.total_days, 0) / calculations.length)
                          : 0
                        }
                      </Typography>
                      <Typography variant="body2">Avg Days</Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Grid>

        {/* Calculation History */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6">Calculation History</Typography>
                <Button variant="outlined" onClick={exportCalculations}>
                  Export CSV
                </Button>
              </Box>

              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Birth Date</TableCell>
                      <TableCell>Target Date</TableCell>
                      <TableCell>Years</TableCell>
                      <TableCell>Months</TableCell>
                      <TableCell>Days</TableCell>
                      <TableCell>Total Days</TableCell>
                      <TableCell>Created</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {calculations.map((calculation) => (
                      <TableRow key={calculation.calculation_id}>
                        <TableCell>{calculation.birth_date}</TableCell>
                        <TableCell>{calculation.target_date}</TableCell>
                        <TableCell>{calculation.years}</TableCell>
                        <TableCell>{calculation.months}</TableCell>
                        <TableCell>{calculation.days}</TableCell>
                        <TableCell>{calculation.total_days}</TableCell>
                        <TableCell>
                          {new Date(calculation.created_at).toLocaleDateString()}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>

              {calculations.length === 0 && (
                <Typography variant="body1" color="textSecondary" align="center" sx={{ mt: 2 }}>
                  No calculations yet. Start by calculating your first age!
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};
