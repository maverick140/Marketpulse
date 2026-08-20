import React, { useEffect, useState } from 'react';
import { AlertTriangle, Building2, Filter, Globe2, ShieldAlert } from 'lucide-react';
import { api } from '../api/client';
import { ProvenanceBadge } from '../components/ProvenanceBadge';
import { GeopoliticalEvent } from '../types';

export const GeopoliticsPage: React.FC = () => {
  const [events, setEvents] = useState<GeopoliticalEvent[]>([]);
  const [regions, setRegions] = useState<any[]>([]);
  const [selectedCountry, setSelectedCountry] = useState('');
  const [selectedSeverity, setSelectedSeverity] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    Promise.allSettled([
      api.getGeopolitics({ country: selectedCountry, severity: selectedSeverity }),
      api.getRegions(),
    ]).then(([eRes, rRes]) => {
      if (eRes.status === 'fulfilled') setEvents(eRes.value.events || []);
      if (rRes.status === 'fulfilled') setRegions(rRes.value.regions || []);
      setLoading(false);
    });
  }, [selectedCountry, selectedSeverity]);

  return (
    <div className="content-wrapper animate-fade">
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '1.5rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.25rem' }}>
            <h1 style={{ fontSize: '1.75rem', fontWeight: 800 }}>Geopolitical Intelligence</h1>
            <ProvenanceBadge status="demo" />
          </div>
          <p style={{ color: '#94a3b8', fontSize: '0.875rem' }}>
            Multi-region conflict, tariff, sanction, and supply-chain surveillance with transparent potential-impact metrics.
          </p>
        </div>
      </div>

      {/* Regional Risk Overview Grid */}
      <div className="grid-cols-4" style={{ marginBottom: '1.5rem' }}>
        {regions.map((reg) => (
          <div key={reg.region} className="card card-hover">
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.4rem' }}>
              <span style={{ fontSize: '0.8125rem', color: '#94a3b8', fontWeight: 600 }}>{reg.region}</span>
              <Globe2 size={16} style={{ color: '#38bdf8' }} />
            </div>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.5rem' }}>
              <span style={{ fontSize: '1.5rem', fontWeight: 800, fontFamily: 'var(--font-mono)' }}>
                {reg.average_severity}
              </span>
              <span style={{ fontSize: '0.75rem', color: '#64748b' }}>/ 100 severity</span>
            </div>
            <p style={{ fontSize: '0.72rem', color: '#64748b', marginTop: '0.4rem' }}>
              {reg.event_count} events • {reg.countries.join(', ')}
            </p>
          </div>
        ))}
      </div>

      {/* Filters Bar */}
      <div className="card" style={{ marginBottom: '1.5rem', padding: '0.85rem 1rem', display: 'flex', gap: '1rem', alignItems: 'center', flexWrap: 'wrap' }}>
        <span style={{ fontSize: '0.8125rem', fontWeight: 600, color: '#94a3b8' }}>Filter Severity:</span>
        <div style={{ display: 'flex', gap: '0.4rem' }}>
          {['', 'LOW', 'MODERATE', 'HIGH', 'CRITICAL'].map((sev) => (
            <button
              key={sev}
              onClick={() => setSelectedSeverity(sev)}
              style={{
                backgroundColor: selectedSeverity === sev ? '#10b981' : '#1e293b',
                color: selectedSeverity === sev ? '#0b0f17' : '#cbd5e1',
                border: 'none',
                padding: '0.35rem 0.7rem',
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
      </div>

      {/* Events Timeline Feed */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {events.map((ev) => (
          <div key={ev.id} className="card card-hover" style={{ borderLeft: `3px solid ${ev.severity >= 70 ? '#ef4444' : ev.severity >= 50 ? '#f59e0b' : '#38bdf8'}` }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.4rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                <span className={`badge ${ev.severity_label === 'CRITICAL' ? 'badge-critical' : ev.severity_label === 'HIGH' ? 'badge-warning' : 'badge-info'}`}>
                  {ev.severity_label} ({ev.severity}/100)
                </span>
                <span className="badge badge-cached">{ev.category}</span>
                <span style={{ fontSize: '0.8125rem', fontWeight: 600, color: '#94a3b8' }}>
                  {ev.country} • {ev.region}
                </span>
              </div>

              <span style={{ fontSize: '0.75rem', color: '#64748b', fontFamily: 'var(--font-mono)' }}>
                Relevance: {ev.market_relevance}/100
              </span>
            </div>

            <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: '#f8fafc', marginBottom: '0.4rem' }}>
              {ev.title}
            </h3>

            {ev.description && (
              <p style={{ fontSize: '0.875rem', color: '#cbd5e1', lineHeight: 1.6, marginBottom: '0.75rem' }}>
                {ev.description}
              </p>
            )}

            {/* Affected Sectors & Assets */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '0.6rem', borderTop: '1px solid #1e293b', flexWrap: 'wrap', gap: '0.5rem' }}>
              <div style={{ display: 'flex', gap: '0.4rem', alignItems: 'center' }}>
                <span style={{ fontSize: '0.75rem', color: '#64748b' }}>Impacted Sectors:</span>
                {ev.related_sectors.map((sec) => (
                  <span key={sec} style={{ backgroundColor: '#1e293b', color: '#38bdf8', padding: '0.15rem 0.45rem', borderRadius: '4px', fontSize: '0.72rem', fontWeight: 600 }}>
                    {sec}
                  </span>
                ))}
              </div>

              <div style={{ display: 'flex', gap: '0.4rem', alignItems: 'center' }}>
                <span style={{ fontSize: '0.75rem', color: '#64748b' }}>Exposed Assets:</span>
                {ev.affected_assets?.map((ast) => (
                  <span key={ast} style={{ backgroundColor: '#1e293b', color: '#34d399', padding: '0.15rem 0.45rem', borderRadius: '4px', fontSize: '0.72rem', fontWeight: 600, fontFamily: 'var(--font-mono)' }}>
                    {ast}
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
