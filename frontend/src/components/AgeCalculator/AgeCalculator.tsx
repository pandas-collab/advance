import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  Paper
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import dayjs, { Dayjs } from 'dayjs';
import { calculateAge } from '../../services/api';
import { ICalculationResult } from '../../types/api';

interface FormData {
  birthDate: Dayjs | null;
  targetDate: Dayjs | null;
  precisionLevel: string;
}

interface FormErrors {
  birthDate?: string;
  targetDate?: string;
  precisionLevel?: string;
}

export const AgeCalculator: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({
    birthDate: null,
    targetDate: dayjs(),
    precisionLevel: 'days'
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [result, setResult] = useState<ICalculationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [submitError, setSubmitError] = useState<string>('');

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    if (!formData.birthDate) {
      newErrors.birthDate = 'Birth date is required';
    }

    if (!formData.targetDate) {
      newErrors.targetDate = 'Target date is required';
    }

    if (formData.birthDate && formData.targetDate &&
        formData.birthDate.isAfter(formData.targetDate)) {
      newErrors.targetDate = 'Target date must be after birth date';
    }

    if (!formData.precisionLevel) {
      newErrors.precisionLevel = 'Precision level is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitError('');

    if (!validateForm()) {
      return;
    }

    setLoading(true);
    try {
      const calculationResult = await calculateAge({
        birth_date: formData.birthDate!.format('YYYY-MM-DD'),
        target_date: formData.targetDate!.format('YYYY-MM-DD'),
        precision_level: formData.precisionLevel
      });
      setResult(calculationResult);
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : 'Calculation failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          Advanced Age Calculator
        </Typography>

        <Card>
          <CardContent>
            <form onSubmit={handleSubmit}>
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <DatePicker
                    label="Birth Date"
                    value={formData.birthDate}
                    onChange={(newValue) => setFormData(prev => ({ ...prev, birthDate: newValue }))}
                    slotProps={{
                      textField: {
                        fullWidth: true,
                        error: !!errors.birthDate,
                        helperText: errors.birthDate
                      }
                    }}
                  />
                </Grid>

                <Grid item xs={12} md={6}>
                  <DatePicker
                    label="Target Date"
                    value={formData.targetDate}
                    onChange={(newValue) => setFormData(prev => ({ ...prev, targetDate: newValue }))}
                    slotProps={{
                      textField: {
                        fullWidth: true,
                        error: !!errors.targetDate,
                        helperText: errors.targetDate
                      }
                    }}
                  />
                </Grid>

                <Grid item xs={12} md={6}>
                  <FormControl fullWidth error={!!errors.precisionLevel}>
                    <InputLabel>Precision Level</InputLabel>
                    <Select
                      value={formData.precisionLevel}
                      label="Precision Level"
                      onChange={(e) => setFormData(prev => ({ ...prev, precisionLevel: e.target.value }))}
                    >
                      <MenuItem value="days">Days</MenuItem>
                      <MenuItem value="hours">Hours</MenuItem>
                      <MenuItem value="minutes">Minutes</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>

                <Grid item xs={12}>
                  <Button
                    type="submit"
                    variant="contained"
                    fullWidth
                    disabled={loading}
                    size="large"
                  >
                    {loading ? 'Calculating...' : 'Calculate Age'}
                  </Button>
                </Grid>
              </Grid>
            </form>

            {submitError && (
              <Alert severity="error" sx={{ mt: 2 }}>
                {submitError}
              </Alert>
            )}

            {result && (
              <Paper sx={{ mt: 3, p: 3, bgcolor: 'primary.light', color: 'primary.contrastText' }}>
                <Typography variant="h5" gutterBottom>
                  Calculation Result
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={6} md={3}>
                    <Typography variant="h6">{result.years}</Typography>
                    <Typography variant="body2">Years</Typography>
                  </Grid>
                  <Grid item xs={6} md={3}>
                    <Typography variant="h6">{result.months}</Typography>
                    <Typography variant="body2">Months</Typography>
                  </Grid>
                  <Grid item xs={6} md={3}>
                    <Typography variant="h6">{result.days}</Typography>
                    <Typography variant="body2">Days</Typography>
                  </Grid>
                  <Grid item xs={6} md={3}>
                    <Typography variant="h6">{result.total_days}</Typography>
                    <Typography variant="body2">Total Days</Typography>
                  </Grid>
                </Grid>
              </Paper>
            )}
          </CardContent>
        </Card>
      </Box>
    </LocalizationProvider>
  );
};
