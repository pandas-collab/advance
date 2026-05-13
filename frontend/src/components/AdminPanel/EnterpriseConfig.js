import React, { useState } from 'react';

const EnterpriseConfig = ({ config, onUpdate }) => {
  const [configData, setConfigData] = useState(config);
  const [saving, setSaving] = useState(false);

  const handleSaveConfig = async () => {
    setSaving(true);
    try {
      const response = await fetch('/api/admin/enterprise-config', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(configData)
      });

      if (response.ok) {
        alert('Configuration saved successfully');
        onUpdate();
      } else {
        throw new Error('Failed to save configuration');
      }
    } catch (error) {
      alert('Error saving configuration: ' + error.message);
    } finally {
      setSaving(false);
    }
  };

  const updateConfig = (section, key, value) => {
    setConfigData({
      ...configData,
      [section]: {
        ...configData[section],
        [key]: value
      }
    });
  };

  return (
    <div className="enterprise-config">
      <h2>Enterprise Configuration</h2>

      <div className="config-sections">
        <div className="config-section">
          <h3>General Settings</h3>
          <div className="config-grid">
            <label>
              Organization Name:
              <input
                type="text"
                value={configData.general?.organizationName || ''}
                onChange={(e) => updateConfig('general', 'organizationName', e.target.value)}
              />
            </label>

            <label>
              Max Users:
              <input
                type="number"
                value={configData.general?.maxUsers || 100}
                onChange={(e) => updateConfig('general', 'maxUsers', parseInt(e.target.value))}
              />
            </label>

            <label>
              Enable Audit Logging:
              <input
                type="checkbox"
                checked={configData.general?.auditLogging || false}
                onChange={(e) => updateConfig('general', 'auditLogging', e.target.checked)}
              />
            </label>

            <label>
              Session Timeout (minutes):
              <input
                type="number"
                value={configData.general?.sessionTimeout || 30}
                onChange={(e) => updateConfig('general', 'sessionTimeout', parseInt(e.target.value))}
              />
            </label>
          </div>
        </div>

        <div className="config-section">
          <h3>Calculation Limits</h3>
          <div className="config-grid">
            <label>
              Max Calculations per User per Day:
              <input
                type="number"
                value={configData.limits?.maxCalculationsPerDay || 1000}
                onChange={(e) => updateConfig('limits', 'maxCalculationsPerDay', parseInt(e.target.value))}
              />
            </label>

            <label>
              Enable Rate Limiting:
              <input
                type="checkbox"
                checked={configData.limits?.enableRateLimit || false}
                onChange={(e) => updateConfig('limits', 'enableRateLimit', e.target.checked)}
              />
            </label>

            <label>
              Max Date Range (years):
              <input
                type="number"
                value={configData.limits?.maxDateRange || 200}
                onChange={(e) => updateConfig('limits', 'maxDateRange', parseInt(e.target.value))}
              />
            </label>
          </div>
        </div>

        <div className="config-section">
          <h3>Security Settings</h3>
          <div className="config-grid">
            <label>
              Require 2FA:
              <input
                type="checkbox"
                checked={configData.security?.require2FA || false}
                onChange={(e) => updateConfig('security', 'require2FA', e.target.checked)}
              />
            </label>

            <label>
              Password Complexity:
              <select
                value={configData.security?.passwordComplexity || 'medium'}
                onChange={(e) => updateConfig('security', 'passwordComplexity', e.target.value)}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </label>

            <label>
              IP Whitelist (comma separated):
              <textarea
                value={configData.security?.ipWhitelist?.join(', ') || ''}
                onChange={(e) => updateConfig('security', 'ipWhitelist',
                  e.target.value.split(',').map(ip => ip.trim()).filter(Boolean))}
                rows="3"
              />
            </label>
          </div>
        </div>

        <div className="config-section">
          <h3>Integration Settings</h3>
          <div className="config-grid">
            <label>
              Enable SAML SSO:
              <input
                type="checkbox"
                checked={configData.integration?.enableSAML || false}
                onChange={(e) => updateConfig('integration', 'enableSAML', e.target.checked)}
              />
            </label>

            <label>
              SAML Issuer URL:
              <input
                type="url"
                value={configData.integration?.samlIssuer || ''}
                onChange={(e) => updateConfig('integration', 'samlIssuer', e.target.value)}
                disabled={!configData.integration?.enableSAML}
              />
            </label>

            <label>
              Webhook Endpoint:
              <input
                type="url"
                value={configData.integration?.webhookUrl || ''}
                onChange={(e) => updateConfig('integration', 'webhookUrl', e.target.value)}
              />
            </label>
          </div>
        </div>
      </div>

      <div className="config-actions">
        <button onClick={handleSaveConfig} disabled={saving} className="save-btn">
          {saving ? 'Saving...' : 'Save Configuration'}
        </button>
        <button onClick={onUpdate} className="reload-btn">
          Reload Configuration
        </button>
      </div>
    </div>
  );
};

export default EnterpriseConfig;
