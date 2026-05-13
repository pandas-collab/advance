import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tabs,
  Tab
} from '@mui/material';
import { ValidationRuleManagement } from './ValidationRuleManagement';
import { ApiKeyManagement } from './ApiKeyManagement';
import { EnterpriseConfiguration } from './EnterpriseConfiguration';

interface AdminPanelProps {
  className?: string;
}

const AdminPanel: React.FC<AdminPanelProps> = ({ className }) => {
  const [activeTab, setActiveTab] = useState<number>(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  return (
    <Box className={className} sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Admin Panel
      </Typography>

      <Paper sx={{ mb: 3 }}>
        <Tabs value={activeTab} onChange={handleTabChange} aria-label="admin panel tabs">
          <Tab label="Dashboard" />
          <Tab label="Enterprise Configuration" />
          <Tab label="Validation Rules" />
          <Tab label="API Keys" />
        </Tabs>
      </Paper>

      {activeTab === 0 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                System Statistics
              </Typography>
              <Typography>Total Calculations: 0</Typography>
              <Typography>Active Users: 0</Typography>
              <Typography>System Status: Online</Typography>
            </Paper>
          </Grid>

          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Quick Actions
              </Typography>
              <Button variant="contained" color="primary" sx={{ mr: 1, mb: 1 }}>
                View Reports
              </Button>
              <Button variant="outlined" color="secondary" sx={{ mr: 1, mb: 1 }}>
                System Settings
              </Button>
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Recent Activity
              </Typography>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Timestamp</TableCell>
                      <TableCell>User</TableCell>
                      <TableCell>Action</TableCell>
                      <TableCell>Status</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    <TableRow>
                      <TableCell colSpan={4} align="center">
                        No recent activity
                      </TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </TableContainer>
            </Paper>
          </Grid>
        </Grid>
      )}

      {activeTab === 1 && <EnterpriseConfiguration />}
      {activeTab === 2 && <ValidationRuleManagement />}
      {activeTab === 3 && <ApiKeyManagement />}
    </Box>
  );
};

export { AdminPanel };
export default AdminPanel;
