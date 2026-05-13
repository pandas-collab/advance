import React, { useState } from 'react';

const ValidationRuleManager = ({ rules, onUpdate }) => {
  const [newRule, setNewRule] = useState({
    name: '',
    description: '',
    condition: '',
    errorMessage: '',
    enabled: true
  });
  const [editing, setEditing] = useState(null);

  const handleCreateRule = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/admin/validation-rules', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newRule)
      });

      if (response.ok) {
        setNewRule({ name: '', description: '', condition: '', errorMessage: '', enabled: true });
        onUpdate();
      } else {
        throw new Error('Failed to create validation rule');
      }
    } catch (error) {
      alert('Error creating rule: ' + error.message);
    }
  };

  const handleDeleteRule = async (ruleId) => {
    if (!confirm('Are you sure you want to delete this rule?')) return;

    try {
      const response = await fetch(`/api/admin/validation-rules/${ruleId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        onUpdate();
      } else {
        throw new Error('Failed to delete validation rule');
      }
    } catch (error) {
      alert('Error deleting rule: ' + error.message);
    }
  };

  const handleToggleRule = async (ruleId, enabled) => {
    try {
      const response = await fetch(`/api/admin/validation-rules/${ruleId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ enabled })
      });

      if (response.ok) {
        onUpdate();
      } else {
        throw new Error('Failed to update validation rule');
      }
    } catch (error) {
      alert('Error updating rule: ' + error.message);
    }
  };

  return (
    <div className="validation-manager">
      <h2>Validation Rule Management</h2>

      <form onSubmit={handleCreateRule} className="rule-form">
        <h3>Create New Validation Rule</h3>
        <div className="form-grid">
          <input
            type="text"
            placeholder="Rule Name"
            value={newRule.name}
            onChange={(e) => setNewRule({...newRule, name: e.target.value})}
            required
          />
          <input
            type="text"
            placeholder="Description"
            value={newRule.description}
            onChange={(e) => setNewRule({...newRule, description: e.target.value})}
            required
          />
          <input
            type="text"
            placeholder="Condition (e.g., age > 0)"
            value={newRule.condition}
            onChange={(e) => setNewRule({...newRule, condition: e.target.value})}
            required
          />
          <input
            type="text"
            placeholder="Error Message"
            value={newRule.errorMessage}
            onChange={(e) => setNewRule({...newRule, errorMessage: e.target.value})}
            required
          />
        </div>
        <button type="submit">Create Rule</button>
      </form>

      <div className="rules-list">
        <h3>Existing Validation Rules</h3>
        {rules.length === 0 ? (
          <p>No validation rules configured.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Description</th>
                <th>Condition</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {rules.map(rule => (
                <tr key={rule.id}>
                  <td>{rule.name}</td>
                  <td>{rule.description}</td>
                  <td><code>{rule.condition}</code></td>
                  <td>
                    <label className="toggle">
                      <input
                        type="checkbox"
                        checked={rule.enabled}
                        onChange={(e) => handleToggleRule(rule.id, e.target.checked)}
                      />
                      <span className="slider"></span>
                    </label>
                  </td>
                  <td>
                    <button onClick={() => handleDeleteRule(rule.id)} className="delete-btn">
                      Delete
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

export default ValidationRuleManager;
