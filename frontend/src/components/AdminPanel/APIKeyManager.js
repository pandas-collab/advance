import React, { useState } from 'react';

const APIKeyManager = ({ apiKeys, onUpdate }) => {
  const [newKey, setNewKey] = useState({
    name: '',
    permissions: [],
    expiresAt: ''
  });

  const availablePermissions = [
    'read:calculations',
    'write:calculations',
    'read:reports',
    'write:reports',
    'admin:config'
  ];

  const handleCreateAPIKey = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/admin/api-keys', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newKey)
      });

      if (response.ok) {
        const result = await response.json();
        alert(`API Key created successfully: ${result.key}`);
        setNewKey({ name: '', permissions: [], expiresAt: '' });
        onUpdate();
      } else {
        throw new Error('Failed to create API key');
      }
    } catch (error) {
      alert('Error creating API key: ' + error.message);
    }
  };

  const handleRevokeKey = async (keyId) => {
    if (!confirm('Are you sure you want to revoke this API key?')) return;

    try {
      const response = await fetch(`/api/admin/api-keys/${keyId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        onUpdate();
      } else {
        throw new Error('Failed to revoke API key');
      }
    } catch (error) {
      alert('Error revoking key: ' + error.message);
    }
  };

  const handlePermissionChange = (permission, checked) => {
    if (checked) {
      setNewKey({
        ...newKey,
        permissions: [...newKey.permissions, permission]
      });
    } else {
      setNewKey({
        ...newKey,
        permissions: newKey.permissions.filter(p => p !== permission)
      });
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="api-key-manager">
      <h2>API Key Management</h2>

      <form onSubmit={handleCreateAPIKey} className="key-form">
        <h3>Generate New API Key</h3>
        <div className="form-group">
          <label>Key Name:</label>
          <input
            type="text"
            placeholder="e.g., Mobile App Integration"
            value={newKey.name}
            onChange={(e) => setNewKey({...newKey, name: e.target.value})}
            required
          />
        </div>

        <div className="form-group">
          <label>Permissions:</label>
          <div className="permissions-grid">
            {availablePermissions.map(permission => (
              <label key={permission} className="permission-checkbox">
                <input
                  type="checkbox"
                  checked={newKey.permissions.includes(permission)}
                  onChange={(e) => handlePermissionChange(permission, e.target.checked)}
                />
                {permission}
              </label>
            ))}
          </div>
        </div>

        <div className="form-group">
          <label>Expires At (optional):</label>
          <input
            type="datetime-local"
            value={newKey.expiresAt}
            onChange={(e) => setNewKey({...newKey, expiresAt: e.target.value})}
          />
        </div>

        <button type="submit">Generate API Key</button>
      </form>

      <div className="keys-list">
        <h3>Active API Keys</h3>
        {apiKeys.length === 0 ? (
          <p>No API keys generated.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Key (masked)</th>
                <th>Permissions</th>
                <th>Created</th>
                <th>Expires</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {apiKeys.map(key => (
                <tr key={key.id}>
                  <td>{key.name}</td>
                  <td><code>{key.maskedKey}</code></td>
                  <td>
                    <div className="permissions-tags">
                      {key.permissions.map(p => (
                        <span key={p} className="permission-tag">{p}</span>
                      ))}
                    </div>
                  </td>
                  <td>{formatDate(key.createdAt)}</td>
                  <td>{key.expiresAt ? formatDate(key.expiresAt) : 'Never'}</td>
                  <td>
                    <span className={`status ${key.status}`}>
                      {key.status}
                    </span>
                  </td>
                  <td>
                    <button
                      onClick={() => handleRevokeKey(key.id)}
                      className="revoke-btn"
                      disabled={key.status === 'revoked'}
                    >
                      Revoke
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default APIKeyManager;
