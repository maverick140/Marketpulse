import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Activity,
  AlertTriangle,
  ArrowRight,
  Building2,
  Cpu,
  Flame,
  Globe2,
  LineChart,
  Shield,
  TrendingDown,
  TrendingUp,
  Zap,
} from 'lucide-react';
import { api } from '../api/client';
import { MetricCard } from '../components/MetricCard';
import { ProvenanceBadge } from '../components/ProvenanceBadge';
import {
  AIInsight,
  Alert,
  MacroIndicator,
  MarketOverview,
  RiskOverview,
  SentimentAnalysis,
} from '../types';

export const DashboardPage: React.FC = () => {
  const [overview, setOverview] = useState<MarketOverview | null>(null);
  const [macro, setMacro] = useState<MacroIndicator[]>([]);
  const [sentiment, setSentiment] = useState<SentimentAnalysis | null>(null);
  const [risk, setRisk] = useState<RiskOverview | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [insights, setInsights] = useState<AIInsight[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const loadAll = async () => {
      try {
        const [ovData, macData, sentData, riskData, alertData, aiData] = await Promise.allSettled([
          api.getMarketOverview(),
          api.getMacroList(),
          api.getMarketSentiment(),
          api.getRiskOverview(),
          api.getAlerts(),
          api.getAIInsights(),
        ]);

        if (ovData.status === 'fulfilled') setOverview(ovData.value);
        if (macData.status === 'fulfilled') setMacro(macData.value.indicators || []);
        if (sentData.status === 'fulfilled') setSentiment(sentData.value);
        if (riskData.status === 'fulfilled') setRisk(riskData.value);
        if (alertData.status === 'fulfilled') setAlerts(alertData.value.alerts || []);
        if (aiData.status === 'fulfilled') setInsights(aiData.value.insights || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    loadAll();
  }, []);

  if (loading) {
    return (
      <div className="content-wrapper">
        <div style={{ display: 'grid', gap: '1rem' }}>
          <div className="skeleton" style={{ height: '40px', width: '280px' }} />
          <div className="grid-cols-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="skeleton" style={{ height: '110px' }} />
            ))}
          </div>
          <div className="grid-cols-2">
            <div className="skeleton" style={{ height: '320px' }} />
            <div className="skeleton" style={{ height: '320px' }} />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="content-wrapper animate-fade">
      {/* Header Banner */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '1.5rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.25rem' }}>
            <h1 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#f8fafc', letterSpacing: '-0.02em' }}>
              Market & Macro Intelligence
            </h1>
            <ProvenanceBadge status={overview?.data_status || 'demo'} />
          </div>
          <p style={{ color: '#94a3b8', fontSize: '0.875rem' }}>
            Real-time multi-factor surveillance combining Indian markets, macroeconomics, sentiment, and geopolitics.
          </p>
        </div>

        <button onClick={() => navigate('/ai-analyst')} className="btn btn-primary">
          <Cpu size={16} />
          Ask AI Analyst
        </button>
      </div>

      {/* 1. Headline Market Indices */}
      <div className="grid-cols-4" style={{ marginBottom: '1.5rem' }}>
        {overview?.indices.map((idx) => (
          <MetricCard
            key={idx.symbol}
            title={idx.name}
            value={idx.value.toLocaleString(undefined, { minimumFractionDigits: 2 })}
            change={idx.change}
            changePercent={idx.change_percent}
            subtitle={`Provider: ${idx.provider.toUpperCase()}`}
            onClick={() => navigate(`/markets?symbol=${idx.symbol}`)}
          />
        ))}
      </div>

      {/* 2. Intelligence Metrics Ribbon: Risk, Sentiment, Inflation, Repo */}
      <div className="grid-cols-4" style={{ marginBottom: '1.5rem' }}>
        <MetricCard
          title="Composite Market Risk"
          value={`${risk?.market_risk_score ?? 38}/100`}
          badge={<span className="badge badge-warning">{risk?.risk_tier ?? 'MODERATE'}</span>}
          subtitle={`Regime: ${risk?.market_regime ?? 'TRENDING_UP'}`}
          icon={<Shield size={16} />}
          onClick={() => navigate('/risk-lab')}
        />

        <MetricCard
          title="Market Sentiment"
          value={sentiment ? `${(sentiment.overall_score > 0 ? '+' : '') + sentiment.overall_score.toFixed(2)}` : '0.00'}
          badge={<span className="badge badge-positive">{sentiment?.overall_label.toUpperCase() ?? 'NEUTRAL'}</span>}
          subtitle={`${sentiment?.total_articles ?? 0} articles analyzed`}
          icon={<Flame size={16} />}
          onClick={() => navigate('/sentiment')}
        />

        <MetricCard
          title="CPI Inflation (Latest)"
          value={macro.find((m) => m.indicator === 'Inflation')?.value ? `${macro.find((m) => m.indicator === 'Inflation')?.value}%` : '4.8%'}
          badge={<span className="badge badge-cached">MACRO</span>}
          subtitle={`Period: ${macro.find((m) => m.indicator === 'Inflation')?.period ?? '2024-05'}`}
          icon={<Building2 size={16} />}
          onClick={() => navigate('/macro?indicator=Inflation')}
        />

        <MetricCard
          title="Crude Oil (Brent)"
          value={`$${macro.find((m) => m.indicator === 'Oil')?.value ?? 82.4}`}
          change={macro.find((m) => m.indicator === 'Oil')?.change}
          subtitle="USD / barrel"
          icon={<Globe2 size={16} />}
          onClick={() => navigate('/macro?indicator=Oil')}
        />
      </div>

      {/* 3. Main Two-Column Dashboard Body */}
      <div className="grid-cols-2" style={{ marginBottom: '1.5rem' }}>
        {/* Left Column: Top Market Movers */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h3 style={{ fontSize: '1rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <LineChart size={18} style={{ color: '#10b981' }} />
              Top Session Movers
            </h3>
            <button onClick={() => navigate('/markets')} style={{ background: 'none', border: 'none', color: '#38bdf8', fontSize: '0.75rem', fontWeight: 600, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.2rem' }}>
              View All <ArrowRight size={12} />
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
            {overview?.gainers.slice(0, 3).map((stock) => (
              <div
                key={stock.symbol}
                onClick={() => navigate(`/markets?symbol=${stock.symbol}`)}
                className="card-hover"
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '0.6rem 0.8rem',
                  borderRadius: '8px',
                  backgroundColor: '#162032',
                  cursor: 'pointer',
                }}
              >
                <div>
                  <p style={{ fontWeight: 700, fontSize: '0.875rem' }}>{stock.symbol}</p>
                  <p style={{ fontSize: '0.75rem', color: '#94a3b8' }}>{stock.name}</p>
                </div>
                <div style={{ textAlign: 'right', fontFamily: 'var(--font-mono)' }}>
                  <p style={{ fontWeight: 700, fontSize: '0.875rem' }}>₹{stock.price.toFixed(2)}</p>
                  <p style={{ color: '#34d399', fontSize: '0.75rem', fontWeight: 600 }}>
                    +{stock.change_percent?.toFixed(2)}%
                  </p>
                </div>
              </div>
            ))}

            {overview?.decliners.slice(0, 2).map((stock) => (
              <div
                key={stock.symbol}
                onClick={() => navigate(`/markets?symbol=${stock.symbol}`)}
                className="card-hover"
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '0.6rem 0.8rem',
                  borderRadius: '8px',
                  backgroundColor: '#162032',
                  cursor: 'pointer',
                }}
              >
                <div>
                  <p style={{ fontWeight: 700, fontSize: '0.875rem' }}>{stock.symbol}</p>
                  <p style={{ fontSize: '0.75rem', color: '#94a3b8' }}>{stock.name}</p>
                </div>
                <div style={{ textAlign: 'right', fontFamily: 'var(--font-mono)' }}>
                  <p style={{ fontWeight: 700, fontSize: '0.875rem' }}>₹{stock.price.toFixed(2)}</p>
                  <p style={{ color: '#f87171', fontSize: '0.75rem', fontWeight: 600 }}>
                    {stock.change_percent?.toFixed(2)}%
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column: AI Contextual Intelligence Digest */}
        <div className="card" style={{ borderColor: 'rgba(6, 182, 212, 0.3)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h3 style={{ fontSize: '1rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#38bdf8' }}>
              <Cpu size={18} />
              AI Intelligence Executive Digest
            </h3>
            <span className="badge badge-info">HYBRID ANALYST</span>
          </div>

          {insights.length > 0 ? (
            <div>
              <p style={{ fontSize: '0.875rem', color: '#cbd5e1', lineHeight: 1.6, marginBottom: '1rem' }}>
                {insights[0].summary}
              </p>

              <div style={{ backgroundColor: '#0b0f17', padding: '0.75rem', borderRadius: '8px', marginBottom: '1rem', border: '1px solid #1e293b' }}>
                <p style={{ fontSize: '0.75rem', fontWeight: 700, color: '#94a3b8', marginBottom: '0.4rem', textTransform: 'uppercase' }}>
                  Grounded Evidence Factors:
                </p>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
                  {insights[0].evidence.slice(0, 3).map((ev, i) => (
                    <div key={i} style={{ fontSize: '0.78rem', color: '#cbd5e1', display: 'flex', gap: '0.4rem' }}>
                      <span style={{ color: '#38bdf8', fontWeight: 600 }}>•</span>
                      <span><strong>{ev.reference}:</strong> {ev.note}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <p style={{ fontSize: '0.7rem', color: '#64748b' }}>
                  {insights[0].disclaimer}
                </p>
                <button onClick={() => navigate('/ai-analyst')} className="btn btn-cyan" style={{ fontSize: '0.75rem', padding: '0.4rem 0.75rem' }}>
                  Open AI Workspace
                </button>
              </div>
            </div>
          ) : (
            <p style={{ color: '#64748b', fontSize: '0.875rem' }}>Loading intelligence context...</p>
          )}
        </div>
      </div>

      {/* 4. Active Alerts & Geopolitical Surveillance Ribbon */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.85rem' }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <AlertTriangle size={18} style={{ color: '#f59e0b' }} />
            Active Surveillance Alerts ({alerts.length})
          </h3>
          <button onClick={() => navigate('/alerts')} style={{ background: 'none', border: 'none', color: '#38bdf8', fontSize: '0.75rem', fontWeight: 600, cursor: 'pointer' }}>
            Manage All Alerts →
          </button>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '0.75rem' }}>
          {alerts.slice(0, 3).map((al) => (
            <div
              key={al.id}
              style={{
                backgroundColor: '#162032',
                borderLeft: `3px solid ${al.severity === 'CRITICAL' ? '#ef4444' : al.severity === 'WARNING' ? '#f59e0b' : '#38bdf8'}`,
                padding: '0.65rem 0.85rem',
                borderRadius: '6px',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.2rem' }}>
                <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#f8fafc' }}>{al.entity}</span>
                <span className={`badge ${al.severity === 'CRITICAL' ? 'badge-critical' : al.severity === 'WARNING' ? 'badge-warning' : 'badge-info'}`}>
                  {al.severity}
                </span>
              </div>
              <p style={{ fontSize: '0.8125rem', color: '#cbd5e1', fontWeight: 500 }}>{al.message}</p>
              <p style={{ fontSize: '0.72rem', color: '#94a3b8', marginTop: '0.2rem' }}>{al.explanation}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
