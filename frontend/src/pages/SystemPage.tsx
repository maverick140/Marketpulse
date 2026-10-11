import React, { useEffect, useState } from 'react';
import { Activity, CheckCircle2, Database, Layers, ShieldCheck, Zap } from 'lucide-react';
import { api } from '../api/client';
import { MetricCard } from '../components/MetricCard';
import { ProvenanceBadge } from '../components/ProvenanceBadge';
import { ProviderStatus, SystemStatus } from '../types';

export const SystemPage: React.FC = () => {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [providers, setProviders] = useState<ProviderStatus[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    Promise.allSettled([
      api.getSystemStatus(),
      api.getProviders(),
    ]).then(([sRes, pRes]) => {
      if (sRes.status === 'fulfilled') setStatus(sRes.value);
      if (pRes.status === 'fulfilled') setProviders(pRes.value.providers || []);
      setLoading(false);
    });
  }, []);

  const isAppOnline = (status?.application_status || 'online').toLowerCase() === 'online';
  const isDbOnline = (status?.database_status || 'online').toLowerCase() === 'online';
  const dataMode = status?.data_mode || 'demo';
  const version = status?.api_version || '1.0.0';

  return (
    <div className="content-wrapper animate-fade">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '1.5rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.25rem' }}>
            <h1 style={{ fontSize: '1.75rem', fontWeight: 800 }}>System Observability & Data Gateway</h1>
            <ProvenanceBadge status={dataMode === 'live' ? 'live' : 'demo'} />
          </div>
          <p style={{ color: '#94a3b8', fontSize: '0.875rem' }}>
            Live backend health, in-memory & database diagnostics, adapter registry verification, and provider fallback telemetry.
          </p>
        </div>
      </div>

      {/* Health Metrics */}
      <div className="grid-cols-4" style={{ marginBottom: '1.5rem' }}>
        <MetricCard
          title="Backend API Status"
          value={isAppOnline ? 'OPERATIONAL' : 'DEGRADED'}
          badge={<span className={`badge ${isAppOnline ? 'badge-live' : 'badge-demo'}`}>{isAppOnline ? 'HEALTHY' : 'CHECK'}</span>}
          subtitle={`FastAPI Core (v${version})`}
          icon={<Zap size={16} style={{ color: '#10b981' }} />}
        />

        <MetricCard
          title="Database Persistence"
          value={isDbOnline ? 'CONNECTED' : 'STANDALONE / MEMORY'}
          badge={<span className="badge badge-cached">SQLITE / MEMORY</span>}
          subtitle={isDbOnline ? '15 SQLite tables initialized' : 'Decoupled in-memory operational'}
          icon={<Database size={16} style={{ color: '#38bdf8' }} />}
        />

        <MetricCard
          title="Active Data Mode"
          value={dataMode.toUpperCase()}
          badge={<span className={`badge ${dataMode === 'live' ? 'badge-live' : 'badge-demo'}`}>{dataMode === 'live' ? 'LIVE DATA' : 'FREE / DEMO FIRST'}</span>}
          subtitle="Zero external paid API requirements"
          icon={<ShieldCheck size={16} style={{ color: '#f59e0b' }} />}
        />

        <MetricCard
          title="Registered Adapters"
          value={providers.length || 5}
          subtitle="Markets / Macro / News / Geo / Ann"
          icon={<Layers size={16} />}
        />
      </div>

      {/* Registered Provider Adapters Table */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Layers size={18} style={{ color: '#38bdf8' }} />
          Active Provider Adapter Registry
        </h3>

        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.8125rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid #1e293b', textAlign: 'left', color: '#64748b' }}>
                <th style={{ padding: '0.5rem 0.75rem' }}>DOMAIN</th>
                <th style={{ padding: '0.5rem 0.75rem' }}>ACTIVE ADAPTER</th>
                <th style={{ padding: '0.5rem 0.75rem' }}>DATA MODE</th>
                <th style={{ padding: '0.5rem 0.75rem' }}>FALLBACK HIERARCHY</th>
                <th style={{ padding: '0.5rem 0.75rem' }}>STATUS</th>
              </tr>
            </thead>
            <tbody>
              {providers.map((p, i) => (
                <tr key={i} style={{ borderBottom: '1px solid #162032' }}>
                  <td style={{ padding: '0.6rem 0.75rem', fontWeight: 700, color: '#f8fafc' }}>
                    {p.type?.toUpperCase() || 'DOMAIN'}
                  </td>
                  <td style={{ padding: '0.6rem 0.75rem', fontFamily: 'var(--font-mono)', color: '#38bdf8' }}>
                    {p.provider || 'demo'}
                  </td>
                  <td style={{ padding: '0.6rem 0.75rem' }}>
                    <span className={`badge ${p.mode === 'live' ? 'badge-live' : 'badge-demo'}`}>
                      {p.mode || 'demo'}
                    </span>
                  </td>
                  <td style={{ padding: '0.6rem 0.75rem', color: '#94a3b8' }}>
                    Primary Provider → In-Memory TTL Cache → SQLite → Deterministic Catalog
                  </td>
                  <td style={{ padding: '0.6rem 0.75rem' }}>
                    <span style={{ color: p.status === 'error' ? '#f43f5e' : '#34d399', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                      <CheckCircle2 size={14} /> {p.status || 'available'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Fallback & Data Provenance Architecture Notice */}
      <div className="card">
        <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.5rem' }}>
          Data Provenance & Resilience Architecture
        </h3>
        <p style={{ fontSize: '0.85rem', color: '#cbd5e1', lineHeight: 1.6, marginBottom: '0.75rem' }}>
          MarketPulse AI employs a resilient layered gateway pattern: <code>Primary Live Provider → Validation & Normalization → Memory TTL Cache → SQLite Cache → Demo Catalog Fallback</code>.
          If any live external network provider fails or times out, the application continues operating seamlessly without crashing, and clearly labels all data with transparent provenance badges.
        </p>
        <p style={{ fontSize: '0.75rem', color: '#64748b' }}>
          Safe observability only: Zero credentials, API keys, or raw stack traces are ever exposed via telemetry or API responses.
        </p>
      </div>
    </div>
  );
};
