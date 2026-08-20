import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Activity,
  ArrowRight,
  Building2,
  Cpu,
  Flame,
  Globe2,
  LineChart,
  Shield,
  Zap,
} from 'lucide-react';

export const LandingPage: React.FC = () => {
  const navigate = useNavigate();

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good Morning, Researcher.';
    if (hour < 17) return 'Good Afternoon, Researcher.';
    return 'Good Evening, Researcher.';
  };

  return (
    <div className="content-wrapper animate-fade" style={{ maxWidth: '1100px', paddingTop: '3rem', paddingBottom: '4rem' }}>
      {/* Hero Banner */}
      <div style={{ textAlign: 'center', marginBottom: '3.5rem' }}>
        <div style={{ marginBottom: '0.75rem' }}>
          <span style={{ fontSize: '1rem', fontWeight: 600, color: '#38bdf8', fontFamily: 'var(--font-mono)' }}>
            {getGreeting()}
          </span>
        </div>

        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem',
            backgroundColor: 'rgba(16, 185, 129, 0.12)',
            border: '1px solid rgba(16, 185, 129, 0.3)',
            color: '#34d399',
            padding: '0.35rem 0.85rem',
            borderRadius: '999px',
            fontSize: '0.8125rem',
            fontWeight: 700,
            marginBottom: '1.25rem',
          }}
        >
          <Activity size={15} />
          Multi-Factor Financial & Geopolitical Intelligence Platform
        </div>

        <h1
          style={{
            fontSize: '3.25rem',
            fontWeight: 900,
            color: '#f8fafc',
            lineHeight: 1.15,
            letterSpacing: '-0.03em',
            marginBottom: '1.25rem',
          }}
        >
          Real-Time Market Signals Grounded in{' '}
          <span style={{ color: '#10b981', textShadow: '0 0 35px rgba(16, 185, 129, 0.35)' }}>
            Empirical Evidence
          </span>
        </h1>

        <p
          style={{
            fontSize: '1.125rem',
            color: '#94a3b8',
            maxWidth: '720px',
            margin: '0 auto 2rem auto',
            lineHeight: 1.6,
          }}
        >
          Synthesize Indian market data, macroeconomic trends, news sentiment NLP, and geopolitical risk into actionable intelligence without mandatory paid APIs.
        </p>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem' }}>
          <button
            onClick={() => navigate('/dashboard')}
            className="btn btn-primary"
            style={{ fontSize: '1rem', padding: '0.75rem 1.75rem' }}
          >
            Launch Intelligence Terminal <ArrowRight size={18} />
          </button>
          <button
            onClick={() => navigate('/ai-analyst')}
            className="btn btn-secondary"
            style={{ fontSize: '1rem', padding: '0.75rem 1.5rem' }}
          >
            <Cpu size={18} /> Explore AI Analyst
          </button>
        </div>
      </div>

      {/* Feature Pillar Cards */}
      <div className="grid-cols-3" style={{ marginBottom: '3rem' }}>
        <div className="card card-hover">
          <LineChart size={28} style={{ color: '#10b981', marginBottom: '0.75rem' }} />
          <h3 style={{ fontSize: '1.125rem', fontWeight: 800, marginBottom: '0.4rem' }}>Indian Markets</h3>
          <p style={{ fontSize: '0.8125rem', color: '#94a3b8', lineHeight: 1.5 }}>
            Equity quotes, OHLCV candlestick series, NIFTY 50, SENSEX, NIFTY IT, and mathematical technical indicators (SMA, EMA, RSI, MACD).
          </p>
        </div>

        <div className="card card-hover">
          <Building2 size={28} style={{ color: '#f59e0b', marginBottom: '0.75rem' }} />
          <h3 style={{ fontSize: '1.125rem', fontWeight: 800, marginBottom: '0.4rem' }}>Macro Surveillance</h3>
          <p style={{ fontSize: '0.8125rem', color: '#94a3b8', lineHeight: 1.5 }}>
            Inflation CPI, RBI policy interest rates, GDP growth, unemployment, crude oil, gold, and INR currency dynamics.
          </p>
        </div>

        <div className="card card-hover">
          <Flame size={28} style={{ color: '#f43f5e', marginBottom: '0.75rem' }} />
          <h3 style={{ fontSize: '1.125rem', fontWeight: 800, marginBottom: '0.4rem' }}>Sentiment NLP</h3>
          <p style={{ fontSize: '0.8125rem', color: '#94a3b8', lineHeight: 1.5 }}>
            Explainable financial lexicon scoring, entity sentiment linking, sector heatmaps, and interactive text sandbox.
          </p>
        </div>

        <div className="card card-hover">
          <Globe2 size={28} style={{ color: '#38bdf8', marginBottom: '0.75rem' }} />
          <h3 style={{ fontSize: '1.125rem', fontWeight: 800, marginBottom: '0.4rem' }}>Geopolitical Risk</h3>
          <p style={{ fontSize: '0.8125rem', color: '#94a3b8', lineHeight: 1.5 }}>
            Regional conflict, tariff, sanction, and supply-chain event monitoring with potential impact scores.
          </p>
        </div>

        <div className="card card-hover">
          <Shield size={28} style={{ color: '#a855f7', marginBottom: '0.75rem' }} />
          <h3 style={{ fontSize: '1.125rem', fontWeight: 800, marginBottom: '0.4rem' }}>Risk Lab & Scenarios</h3>
          <p style={{ fontSize: '0.8125rem', color: '#94a3b8', lineHeight: 1.5 }}>
            Composite risk gauge (0-100), market regime classification, correlation matrices, and macroeconomic stress testing.
          </p>
        </div>

        <div className="card card-hover">
          <Cpu size={28} style={{ color: '#06b6d4', marginBottom: '0.75rem' }} />
          <h3 style={{ fontSize: '1.125rem', fontWeight: 800, marginBottom: '0.4rem' }}>AI Research Engine</h3>
          <p style={{ fontSize: '0.8125rem', color: '#94a3b8', lineHeight: 1.5 }}>
            Grounded contextual research answering natural language queries with concrete empirical evidence and uncertainty bounds.
          </p>
        </div>
      </div>
    </div>
  );
};
