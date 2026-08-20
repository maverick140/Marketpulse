import React, { useEffect, useState } from 'react';
import {
  Activity,
  AlertOctagon,
  Flame,
  Globe2,
  Play,
  Shield,
  ShieldAlert,
  Sliders,
  TrendingDown,
  TrendingUp,
} from 'lucide-react';
import { api } from '../api/client';
import { MetricCard } from '../components/MetricCard';
import { ProvenanceBadge } from '../components/ProvenanceBadge';
import { RiskOverview, ScenarioResult } from '../types';

export const RiskLabPage: React.FC = () => {
  const [risk, setRisk] = useState<RiskOverview | null>(null);
  const [correlation, setCorrelation] = useState<{ assets: string[]; matrix: number[][] } | null>(null);
  const [scenarioType, setScenarioType] = useState('Crude Oil Surge');
  const [magnitude, setMagnitude] = useState(20);
  const [scenarioResult, setScenarioResult] = useState<ScenarioResult | null>(null);
  const [simulating, setSimulating] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    Promise.allSettled([
      api.getRiskOverview(),
      api.getCorrelation(),
      api.simulateScenario('Crude Oil Surge', 20),
    ]).then(([rRes, cRes, sRes]) => {
      if (rRes.status === 'fulfilled') setRisk(rRes.value);
      if (cRes.status === 'fulfilled') setCorrelation(cRes.value);
      if (sRes.status === 'fulfilled') setScenarioResult(sRes.value);
      setLoading(false);
    });
  }, []);

  const handleRunSimulation = async () => {
    setSimulating(true);
    try {
      const res = await api.simulateScenario(scenarioType, magnitude);
      setScenarioResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setSimulating(false);
    }
  };

  return (
    <div className="content-wrapper animate-fade">
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '1.5rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.25rem' }}>
            <h1 style={{ fontSize: '1.75rem', fontWeight: 800 }}>Risk & Scenario Lab</h1>
            <span className="badge badge-warning">QUANT RISK ENGINE</span>
          </div>
          <p style={{ color: '#94a3b8', fontSize: '0.875rem' }}>
            Multi-factor composite risk metrics, regime classification, stress testing, and asset correlation matrix.
          </p>
        </div>
      </div>

      {/* Top Risk Metrics */}
      <div className="grid-cols-4" style={{ marginBottom: '1.5rem' }}>
        <MetricCard
          title="Composite Market Risk"
          value={`${risk?.market_risk_score ?? 38}/100`}
          badge={<span className={`badge ${risk?.risk_tier === 'HIGH' || risk?.risk_tier === 'VERY_HIGH' ? 'badge-critical' : 'badge-warning'}`}>{risk?.risk_tier ?? 'MODERATE'}</span>}
          subtitle="Scaled 0 (Safe) to 100 (High Risk)"
          icon={<Shield size={16} />}
        />
        <MetricCard
          title="Market Regime"
          value={risk?.market_regime ?? 'TRENDING_UP'}
          badge={<span className="badge badge-cached">REGIME</span>}
          subtitle="Determined via price trend & volatility"
          icon={<Activity size={16} />}
        />
        <MetricCard
          title="Annualized Volatility"
          value={`${risk?.volatility_index ? risk.volatility_index.toFixed(1) : '16.5'}%`}
          subtitle="30-day NIFTY 50 realized volatility"
        />
        <MetricCard
          title="Sector Risk Variance"
          value="5 Sectors"
          subtitle="Energy / Tech / Banks / FMCG / Infra"
        />
      </div>

      {/* Main Two Column Body: Stress Simulator & Correlation Matrix */}
      <div className="grid-cols-2" style={{ marginBottom: '1.5rem' }}>
        {/* Left: Stress Scenario Simulator */}
        <div className="card" style={{ borderColor: 'rgba(245, 158, 11, 0.3)' }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.6rem', color: '#fbbf24', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Sliders size={18} />
            Macro & Geopolitical Shock Simulator
          </h3>
          <p style={{ fontSize: '0.8125rem', color: '#94a3b8', marginBottom: '1rem' }}>
            Simulate historical or hypothetical macroeconomic shocks to evaluate sectoral price sensitivity.
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', marginBottom: '1rem' }}>
            <div>
              <label style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: 600, display: 'block', marginBottom: '0.3rem' }}>
                SCENARIO TYPE
              </label>
              <select
                className="input"
                value={scenarioType}
                onChange={(e) => setScenarioType(e.target.value)}
                style={{ fontSize: '0.875rem' }}
              >
                <option value="Crude Oil Surge">Crude Oil Surge (+20% Shock)</option>
                <option value="Interest Rate Hike">Central Bank Rate Hike (+50 bps)</option>
                <option value="Geopolitical Disruption">Regional Geopolitical Supply Disruption</option>
                <option value="Broad Market Correction">Global Equity Market Correction (-5%)</option>
              </select>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.3rem' }}>
                <label style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: 600 }}>SHOCK MAGNITUDE</label>
                <span style={{ fontSize: '0.8125rem', fontWeight: 700, fontFamily: 'var(--font-mono)', color: '#f8fafc' }}>
                  {magnitude > 0 ? `+${magnitude}` : magnitude}%
                </span>
              </div>
              <input
                type="range"
                min="-30"
                max="50"
                step="5"
                value={magnitude}
                onChange={(e) => setMagnitude(Number(e.target.value))}
                style={{ width: '100%', accentColor: '#10b981' }}
              />
            </div>

            <button onClick={handleRunSimulation} disabled={simulating} className="btn btn-primary" style={{ marginTop: '0.5rem' }}>
              <Play size={14} />
              {simulating ? 'Computing Shock Models...' : 'Execute Stress Simulation'}
            </button>
          </div>

          {/* Simulation Output */}
          {scenarioResult && (
            <div style={{ backgroundColor: '#0b0f17', padding: '1rem', borderRadius: '8px', border: '1px solid #1e293b' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '0.5rem' }}>
                <span style={{ fontSize: '0.8125rem', fontWeight: 700, color: '#f8fafc' }}>Est. Market Impact:</span>
                <span style={{ fontSize: '1.125rem', fontWeight: 800, fontFamily: 'var(--font-mono)', color: scenarioResult.estimated_market_impact_percent >= 0 ? '#34d399' : '#f87171' }}>
                  {scenarioResult.estimated_market_impact_percent >= 0 ? '+' : ''}{scenarioResult.estimated_market_impact_percent.toFixed(2)}%
                </span>
              </div>

              <p style={{ fontSize: '0.8125rem', color: '#cbd5e1', lineHeight: 1.5, marginBottom: '0.75rem' }}>
                {scenarioResult.summary}
              </p>

              {/* Sector Impacts */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
                {Object.entries(scenarioResult.sector_impacts).map(([sec, imp]) => (
                  <div key={sec} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem' }}>
                    <span style={{ color: '#94a3b8' }}>{sec}</span>
                    <span style={{ fontWeight: 700, fontFamily: 'var(--font-mono)', color: imp >= 0 ? '#34d399' : '#f87171' }}>
                      {imp >= 0 ? '+' : ''}{imp.toFixed(2)}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Right: Correlation Matrix */}
        <div className="card">
          <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.6rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Activity size={18} style={{ color: '#38bdf8' }} />
            Asset & Index Correlation Matrix
          </h3>
          <p style={{ fontSize: '0.8125rem', color: '#94a3b8', marginBottom: '1rem' }}>
            Pairwise Pearson correlation coefficient calculated across 30-day daily price returns.
          </p>

          {correlation ? (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.75rem', fontFamily: 'var(--font-mono)' }}>
                <thead>
                  <tr style={{ borderBottom: '1px solid #1e293b' }}>
                    <th style={{ padding: '0.4rem', textAlign: 'left', color: '#64748b' }}>ASSET</th>
                    {correlation.assets.map((a) => (
                      <th key={a} style={{ padding: '0.4rem', textAlign: 'center', color: '#64748b' }}>
                        {a.split(' ')[0]}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {correlation.matrix.map((row, i) => (
                    <tr key={i} style={{ borderBottom: '1px solid #162032' }}>
                      <td style={{ padding: '0.4rem', fontWeight: 700, color: '#94a3b8' }}>
                        {correlation.assets[i].split(' ')[0]}
                      </td>
                      {row.map((val, j) => {
                        const isSelf = i === j;
                        return (
                          <td
                            key={j}
                            style={{
                              padding: '0.4rem',
                              textAlign: 'center',
                              fontWeight: 600,
                              color: isSelf ? '#64748b' : val > 0.6 ? '#34d399' : val < 0 ? '#f87171' : '#f8fafc',
                              backgroundColor: isSelf ? 'transparent' : val > 0.6 ? 'rgba(16, 185, 129, 0.1)' : 'transparent',
                            }}
                          >
                            {val.toFixed(2)}
                          </td>
                        );
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p style={{ color: '#64748b', fontSize: '0.875rem' }}>Loading correlation matrix...</p>
          )}
        </div>
      </div>
    </div>
  );
};
