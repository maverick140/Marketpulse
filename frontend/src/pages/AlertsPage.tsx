import React, { useEffect, useState } from 'react';
import { AlertCircle, AlertOctagon, AlertTriangle, Bell, Info, Shield } from 'lucide-react';
import { api } from '../api/client';
import { MetricCard } from '../components/MetricCard';
import { ProvenanceBadge } from '../components/ProvenanceBadge';
import { Alert } from '../types';

export const AlertsPage: React.FC = () => {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [counts, setCounts] = useState({ total: 0, critical: 0, warning: 0, info: 0 });
  const [selectedSeverity, setSelectedSeverity] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api.getAlerts(selectedSeverity)
      .then((res) => {
        setAlerts(res.alerts || []);
        setCounts({
          total: res.total || 0,
          critical: res.critical_count || 0,
          warning: res.warning_count || 0,
          info: res.info_count || 0,
        });
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [selectedSeverity]);

  return (
    <div className="content-wrapper animate-fade">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '1.5rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.25rem' }}>
            <h1 style={{ fontSize: '1.75rem', fontWeight: 800 }}>Intelligence Alerts & Monitoring</h1>
            <ProvenanceBadge status="demo" />
          </div>
          <p style={{ color: '#94a3b8', fontSize: '0.875rem' }}>
            Rule-based threshold alerts covering price breakouts, volume surges, geopolitical developments, and macro calendar releases.
          </p>
        </div>
      </div>

      {/* Counts Ribbon */}
      <div className="grid-cols-4" style={{ marginBottom: '1.5rem' }}>
        <MetricCard title="Total Active Alerts" value={counts.total} icon={<Bell size={16} />} />
        <MetricCard
          title="Critical Alerts"
          value={counts.critical}
          badge={<span className="badge badge-critical">CRITICAL</span>}
          variant="ruby"
          icon={<AlertOctagon size={16} style={{ color: '#f43f5e' }} />}
        />
        <MetricCard
          title="Warning Alerts"
          value={counts.warning}
          badge={<span className="badge badge-warning">WARNING</span>}
          icon={<AlertTriangle size={16} style={{ color: '#f59e0b' }} />}
        />
        <MetricCard
          title="Informational Signals"
          value={counts.info}
          badge={<span className="badge badge-info">INFO</span>}
          icon={<Info size={16} style={{ color: '#06b6d4' }} />}
        />
      </div>

      {/* Severity Filter */}
      <div style={{ display: 'flex', gap: '0.4rem', marginBottom: '1.5rem' }}>
        {['', 'CRITICAL', 'WARNING', 'INFO'].map((sev) => (
          <button
            key={sev}
            onClick={() => setSelectedSeverity(sev)}
            style={{
              backgroundColor: selectedSeverity === sev ? '#10b981' : '#1e293b',
              color: selectedSeverity === sev ? '#0b0f17' : '#cbd5e1',
              border: 'none',
              padding: '0.4rem 0.8rem',
              borderRadius: '6px',
              fontSize: '0.75rem',
              fontWeight: 700,
              cursor: 'pointer',
            }}
          >
            {sev || 'ALL SEVERITIES'}
          </button>
        ))}
      </div>

      {/* Alerts Feed */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
        {alerts.map((al) => (
          <div
            key={al.id}
            className="card card-hover"
            style={{
              borderLeft: `4px solid ${
                al.severity === 'CRITICAL' ? '#ef4444' : al.severity === 'WARNING' ? '#f59e0b' : '#06b6d4'
              }`,
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.35rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                <span className={`badge ${al.severity === 'CRITICAL' ? 'badge-critical' : al.severity === 'WARNING' ? 'badge-warning' : 'badge-info'}`}>
                  {al.severity}
                </span>
                <span className="badge badge-cached">{al.alert_type}</span>
                <span style={{ fontSize: '0.8125rem', fontWeight: 700, color: '#f8fafc' }}>
                  {al.entity}
                </span>
              </div>
              <span style={{ fontSize: '0.75rem', color: '#64748b', fontFamily: 'var(--font-mono)' }}>
                {new Date(al.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>

            <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#f8fafc', marginBottom: '0.3rem' }}>
              {al.message}
            </h3>

            <p style={{ fontSize: '0.8125rem', color: '#94a3b8' }}>
              {al.explanation}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};
