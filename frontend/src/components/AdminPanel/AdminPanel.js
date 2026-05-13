import React, { useState, useEffect } from 'react';
import ValidationRuleManager from './ValidationRuleManager';
import APIKeyManager from './APIKeyManager';
import EnterpriseConfig from './EnterpriseConfig';
import './AdminPanel.css';

const AdminPanel = () => {
  const [activeTab, setActiveTab] = useState('validation');
  const [adminData, setAdminData] = useState({
    validationRules: [],
    apiKeys: [],
    enterpriseConfig: {}
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadAdminData();
  }, []);

  const loadAdminData = async () => {
    try {
      setLoading(true);
      // Load admin data from API
      const [rules, keys, config] = await Promise.all([
        fetch('/api/admin/validation-rules').then(r => r.json()),
        fetch('/api/admin/api-keys').then(r => r.json()),
        fetch('/api/admin/enterprise-config').then(r => r.json())
      ]);

      setAdminData({
        validationRules: rules,
        apiKeys: keys,
        enterpriseConfig: config
      });
    } catch (err) {
      setError('Failed to load admin data: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="admin-loading">Loading admin panel...</div>;
  if (error) return <div className="admin-error">{error}</div>;

  return (
    <div className="admin-panel">
      <div className="admin-header">
        <h1>Admin Panel</h1>
        <p>Enterprise Configuration & Management</p>
      </div>

      <div className="admin-tabs">
        <button
          className={activeTab === 'validation' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('validation')}
        >
          Validation Rules
        </button>
        <button
          className={activeTab === 'apikeys' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('apikeys')}
        >
          API Keys
        </button>
        <button
          className={activeTab === 'config' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('config')}
        >
          Enterprise Config
        </button>
      </div>

      <div className="admin-content">
        {activeTab === 'validation' && (
          <ValidationRuleManager
            rules={adminData.validationRules}
            onUpdate={loadAdminData}
          />
        )}
        {activeTab === 'apikeys' && (
          <APIKeyManager
            apiKeys={adminData.apiKeys}
            onUpdate={loadAdminData}
          />
        )}
        {activeTab === 'config' && (
          <EnterpriseConfig
            config={adminData.enterpriseConfig}
            onUpdate={loadAdminData}
          />
        )}
      </div>
    </div>
  );
};

export default AdminPanel;
