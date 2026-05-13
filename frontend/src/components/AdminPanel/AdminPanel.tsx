import React, { useState } from 'react';
import { ValidationRuleManagement } from './ValidationRuleManagement';
import { ApiKeyManagement } from './ApiKeyManagement';
import { EnterpriseConfiguration } from './EnterpriseConfiguration';

interface AdminPanelProps {
  className?: string;
}

export const AdminPanel: React.FC<AdminPanelProps> = ({ className }) => {
  const [activeTab, setActiveTab] = useState<'config' | 'validation' | 'apikeys'>('config');

  return (
    <div className={`admin-panel ${className || ''}`}>
      <div className="admin-header">
        <h1>Admin Panel</h1>
        <nav className="admin-nav">
          <button
            className={activeTab === 'config' ? 'active' : ''}
            onClick={() => setActiveTab('config')}
          >
            Enterprise Configuration
          </button>
          <button
            className={activeTab === 'validation' ? 'active' : ''}
            onClick={() => setActiveTab('validation')}
          >
            Validation Rules
          </button>
          <button
            className={activeTab === 'apikeys' ? 'active' : ''}
            onClick={() => setActiveTab('apikeys')}
          >
            API Keys
          </button>
        </nav>
      </div>

      <div className="admin-content">
        {activeTab === 'config' && <EnterpriseConfiguration />}
        {activeTab === 'validation' && <ValidationRuleManagement />}
        {activeTab === 'apikeys' && <ApiKeyManagement />}
      </div>
    </div>
  );
};

export default AdminPanel;
