import React from 'react';
import {
  Activity,
  Award,
  BookOpen,
  Code2,
  Cpu,
  Database,
  Globe2,
  HelpCircle,
  Layers,
  LineChart,
  Lock,
  Shield,
  Zap,
} from 'lucide-react';

interface Props {
  onOpenDisclaimer: () => void;
}

export const AboutPage: React.FC<Props> = ({ onOpenDisclaimer }) => {
  return (
    <div className="content-wrapper animate-fade" style={{ maxWidth: '1000px' }}>
      {/* Header */}
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 800, color: '#f8fafc', letterSpacing: '-0.02em', marginBottom: '0.5rem' }}>
          About MarketPulse AI
        </h1>
        <p style={{ fontSize: '1rem', color: '#94a3b8', lineHeight: 1.6 }}>
          A full-stack financial and geopolitical intelligence platform combining Indian equity data, macroeconomic surveillance, explainable sentiment NLP, and evidence-grounded AI research.
        </p>
      </div>

      {/* Highlights Grid */}
      <div className="grid-cols-3" style={{ marginBottom: '2rem' }}>
        <div className="card">
          <Code2 size={24} style={{ color: '#10b981', marginBottom: '0.75rem' }} />
          <h3 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '0.4rem' }}>Layered Architecture</h3>
          <p style={{ fontSize: '0.8125rem', color: '#94a3b8', lineHeight: 1.5 }}>
            Clean separation of FastAPI routes, Pydantic schemas, modular services, DataGateway, provider adapters, and SQLite persistence.
          </p>
        </div>

        <div className="card">
          <Shield size={24} style={{ color: '#38bdf8', marginBottom: '0.75rem' }} />
          <h3 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '0.4rem' }}>Free-First & Demo Fallback</h3>
          <p style={{ fontSize: '0.8125rem', color: '#94a3b8', lineHeight: 1.5 }}>
            Runs reliably without mandatory paid subscriptions. When live feeds fail, gracefully switches to cache and synthetic catalogs.
          </p>
        </div>

        <div className="card">
          <Cpu size={24} style={{ color: '#c084fc', marginBottom: '0.75rem' }} />
          <h3 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '0.4rem' }}>Explainable AI & ML</h3>
          <p style={{ fontSize: '0.8125rem', color: '#94a3b8', lineHeight: 1.5 }}>
            Factual multi-factor synthesis citing concrete market, macro, and news evidence with explicit uncertainty boundaries.
          </p>
        </div>
      </div>

      {/* Compliance & Educational Disclaimers */}
      <div className="card" style={{ marginBottom: '2rem', borderColor: 'rgba(245, 158, 11, 0.4)' }}>
        <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: '#fbbf24', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Shield size={20} />
          Compliance, Scope & Educational Notice
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.85rem', color: '#cbd5e1', lineHeight: 1.6 }}>
          <p>
            <strong>1. Educational Portfolio Demonstration:</strong> MarketPulse AI is designed solely for computer science, machine learning, and financial engineering portfolio demonstrations.
          </p>
          <p>
            <strong>2. Regulatory Positioning:</strong> MarketPulse AI is <em>NOT</em> registered with the Securities and Exchange Board of India (SEBI), US SEC, or any financial regulatory body.
          </p>
          <p>
            <strong>3. No Financial Advice:</strong> This application does not issue Buy, Sell, or Hold recommendations, guaranteed returns, or automated trading execution.
          </p>
        </div>

        <div style={{ marginTop: '1.25rem', paddingTop: '1rem', borderTop: '1px solid #1e293b' }}>
          <button onClick={onOpenDisclaimer} className="btn btn-secondary">
            <HelpCircle size={15} /> Reopen Full Legal Disclaimer Modal
          </button>
        </div>
      </div>

      {/* Creator Attribution */}
      <div
        style={{
          marginTop: '3rem',
          paddingTop: '1.5rem',
          borderTop: '1px solid #1e293b',
          textAlign: 'center',
        }}
      >
        <p
          style={{
            fontSize: '0.875rem',
            color: '#94a3b8',
            fontWeight: 500,
            letterSpacing: '0.01em',
          }}
        >
          Built with <span style={{ color: '#ef4444', margin: '0 0.15rem' }}>❤️</span> by <strong style={{ color: '#f8fafc', fontWeight: 600 }}>Manan</strong>
        </p>
      </div>
    </div>
  );
};
