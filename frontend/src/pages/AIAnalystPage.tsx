import React, { useEffect, useState } from 'react';
import {
  AlertTriangle,
  Bookmark,
  CheckCircle2,
  Cpu,
  FileText,
  HelpCircle,
  Info,
  Play,
  Send,
  ShieldAlert,
  Sparkles,
} from 'lucide-react';
import { api } from '../api/client';
import { ProvenanceBadge } from '../components/ProvenanceBadge';
import { AIInsight } from '../types';

export const AIAnalystPage: React.FC = () => {
  const [query, setQuery] = useState('What are the key macroeconomic and geopolitical factors impacting the Indian market setup?');
  const [currentInsight, setCurrentInsight] = useState<AIInsight | null>(null);
  const [loading, setLoading] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);

  useEffect(() => {
    // Initial fetch of default pre-compiled insight
    setLoading(true);
    api.getAIInsights()
      .then((res) => {
        if (res.insights && res.insights.length > 0) {
          setCurrentInsight(res.insights[0]);
        }
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const handleResearch = async (customQ?: string) => {
    const targetQ = customQ || query;
    if (!targetQ.trim()) return;
    setLoading(true);
    setSavedSuccess(false);
    try {
      const res = await api.runAIResearch({ query: targetQ });
      setCurrentInsight(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveToWorkspace = async () => {
    if (!currentInsight) return;
    try {
      await api.saveResearch({
        title: currentInsight.query.slice(0, 48),
        query: currentInsight.query,
        summary: currentInsight.summary,
        tags: ['AI Analysis', 'Macro', 'Surveillance'],
      });
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
    } catch (e) {
      console.error(e);
    }
  };

  const SAMPLE_PROMPTS = [
    'Why is NIFTY moving today?',
    'What is happening with crude oil?',
    'Explain the latest geopolitical risks affecting markets.',
    'What are the main risks for Indian equities right now?',
    'What could cause the Indian rupee to weaken?',
    'Explain the difference between NIFTY and SENSEX.',
    'Technology Sector & Export Demand Outlook',
  ];

  return (
    <div className="content-wrapper animate-fade">
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '1.25rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.25rem' }}>
            <h1 style={{ fontSize: '1.75rem', fontWeight: 800 }}>AI Intelligence & Research Analyst</h1>
            <span className="badge badge-warning">LIMITED-SCOPE ANALYST</span>
          </div>
          <p style={{ color: '#94a3b8', fontSize: '0.875rem' }}>
            Factual, evidence-grounded research synthesis combining real-time markets, macro data, sentiment, and geopolitics.
          </p>
        </div>
      </div>

      {/* Subtle Limited-Scope Disclaimer Banner */}
      <div
        style={{
          display: 'flex',
          alignItems: 'flex-start',
          gap: '0.75rem',
          backgroundColor: 'rgba(30, 41, 59, 0.4)',
          border: '1px solid #1e293b',
          borderRadius: '8px',
          padding: '0.85rem 1.1rem',
          marginBottom: '1.5rem',
          fontSize: '0.8125rem',
          color: '#94a3b8',
          lineHeight: 1.5,
        }}
      >
        <Info size={16} style={{ color: '#38bdf8', marginTop: '0.15rem', flexShrink: 0 }} />
        <div>
          <p style={{ color: '#cbd5e1', marginBottom: '0.25rem' }}>
            <strong>AI Analyst is a limited-scope research synthesizer.</strong> It works with the market, macroeconomic, news, sentiment, and geopolitical data currently available to MarketPulse AI. It may not be able to answer every financial or market question accurately.
          </p>
          <p style={{ fontSize: '0.75rem', color: '#64748b' }}>
            AI-generated responses are for educational and research purposes only and are not financial, investment, or trading advice. Always verify important information with reliable primary sources.
          </p>
        </div>
      </div>

      {/* Query Bar */}
      <div className="card" style={{ marginBottom: '1.5rem', borderColor: 'rgba(6, 182, 212, 0.3)' }}>
        <div style={{ display: 'flex', gap: '0.75rem', marginBottom: '0.75rem' }}>
          <input
            type="text"
            className="input"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleResearch()}
            placeholder="Ask AI Analyst for contextual financial analysis..."
            style={{ fontSize: '0.95rem' }}
          />
          <button onClick={() => handleResearch()} disabled={loading} className="btn btn-primary" style={{ whiteSpace: 'nowrap' }}>
            <Send size={15} />
            {loading ? 'Synthesizing...' : 'Run Research'}
          </button>
        </div>

        {/* Suggested Prompt Chips */}
        <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap', alignItems: 'center' }}>
          <span style={{ fontSize: '0.72rem', color: '#64748b', fontWeight: 600 }}>Try asking:</span>
          {SAMPLE_PROMPTS.map((p) => (
            <button
              key={p}
              onClick={() => {
                setQuery(p);
                handleResearch(p);
              }}
              style={{
                backgroundColor: '#162032',
                border: '1px solid #1e293b',
                color: '#94a3b8',
                padding: '0.2rem 0.55rem',
                borderRadius: '6px',
                fontSize: '0.75rem',
                cursor: 'pointer',
              }}
            >
              {p}
            </button>
          ))}
        </div>
      </div>

      {/* Structured Analysis Response Display */}
      {loading ? (
        <div className="card" style={{ padding: '2rem' }}>
          <div className="skeleton" style={{ height: '30px', width: '300px', marginBottom: '1rem' }} />
          <div className="skeleton" style={{ height: '80px', marginBottom: '1rem' }} />
          <div className="skeleton" style={{ height: '140px' }} />
        </div>
      ) : currentInsight ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          {/* Executive Summary Card */}
          <div className="card" style={{ borderColor: 'rgba(16, 185, 129, 0.3)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
              <div>
                <span style={{ fontSize: '0.75rem', color: '#10b981', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  Executive Intelligence Summary
                </span>
                <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#f8fafc', marginTop: '0.2rem' }}>
                  {currentInsight.query}
                </h2>
              </div>

              <button
                onClick={handleSaveToWorkspace}
                className="btn btn-secondary"
                style={{ fontSize: '0.75rem', padding: '0.35rem 0.75rem' }}
              >
                {savedSuccess ? <CheckCircle2 size={14} style={{ color: '#34d399' }} /> : <Bookmark size={14} />}
                {savedSuccess ? 'Saved to Workspace' : 'Save Research'}
              </button>
            </div>

            <p style={{ fontSize: '0.95rem', color: '#f1f5f9', lineHeight: 1.7, marginBottom: '1rem' }}>
              {currentInsight.summary}
            </p>

            <div style={{ padding: '0.75rem 1rem', backgroundColor: '#0b0f17', borderRadius: '8px', border: '1px solid #1e293b' }}>
              <p style={{ fontSize: '0.85rem', color: '#cbd5e1', lineHeight: 1.6 }}>
                <strong>Market Context:</strong> {currentInsight.market_context}
              </p>
            </div>
          </div>

          {/* Factor Breakdown Grid */}
          <div className="grid-cols-3">
            {/* Macro Factors */}
            <div className="card">
              <h4 style={{ fontSize: '0.875rem', fontWeight: 700, color: '#f59e0b', marginBottom: '0.6rem' }}>
                Macro Factors
              </h4>
              <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.45rem' }}>
                {currentInsight.macro_factors.map((m, i) => (
                  <li key={i} style={{ fontSize: '0.8125rem', color: '#cbd5e1', display: 'flex', gap: '0.4rem' }}>
                    <span style={{ color: '#f59e0b' }}>•</span>
                    <span>{m}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Geopolitical Factors */}
            <div className="card">
              <h4 style={{ fontSize: '0.875rem', fontWeight: 700, color: '#f43f5e', marginBottom: '0.6rem' }}>
                Geopolitical Factors
              </h4>
              <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.45rem' }}>
                {currentInsight.geopolitical_factors.map((g, i) => (
                  <li key={i} style={{ fontSize: '0.8125rem', color: '#cbd5e1', display: 'flex', gap: '0.4rem' }}>
                    <span style={{ color: '#f43f5e' }}>•</span>
                    <span>{g}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Risk & Uncertainties */}
            <div className="card">
              <h4 style={{ fontSize: '0.875rem', fontWeight: 700, color: '#c084fc', marginBottom: '0.6rem' }}>
                Identified Uncertainties
              </h4>
              <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.45rem' }}>
                {currentInsight.uncertainties.map((u, i) => (
                  <li key={i} style={{ fontSize: '0.8125rem', color: '#cbd5e1', display: 'flex', gap: '0.4rem' }}>
                    <span style={{ color: '#c084fc' }}>•</span>
                    <span>{u}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Grounded Evidence Table */}
          <div className="card">
            <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <FileText size={18} style={{ color: '#38bdf8' }} />
              Grounded Empirical Evidence Base
            </h3>

            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.8125rem' }}>
                <thead>
                  <tr style={{ borderBottom: '1px solid #1e293b', textAlign: 'left', color: '#64748b' }}>
                    <th style={{ padding: '0.5rem 0.75rem' }}>DOMAIN</th>
                    <th style={{ padding: '0.5rem 0.75rem' }}>REFERENCE DATA POINT</th>
                    <th style={{ padding: '0.5rem 0.75rem' }}>ANALYST INTERPRETATION</th>
                  </tr>
                </thead>
                <tbody>
                  {currentInsight.evidence.map((ev, i) => (
                    <tr key={i} style={{ borderBottom: '1px solid #162032' }}>
                      <td style={{ padding: '0.6rem 0.75rem', fontWeight: 700, color: '#38bdf8' }}>
                        {ev.source_type.toUpperCase()}
                      </td>
                      <td style={{ padding: '0.6rem 0.75rem', color: '#f8fafc', fontWeight: 600, fontFamily: 'var(--font-mono)' }}>
                        {ev.reference}
                      </td>
                      <td style={{ padding: '0.6rem 0.75rem', color: '#94a3b8' }}>
                        {ev.note}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Disclaimer Ribbon */}
          <div style={{ backgroundColor: '#0b0f17', padding: '0.75rem 1rem', borderRadius: '8px', border: '1px solid #1e293b', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <ShieldAlert size={18} style={{ color: '#f59e0b', flexShrink: 0 }} />
            <p style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
              <strong>Compliance Notice:</strong> {currentInsight.disclaimer}
            </p>
          </div>
        </div>
      ) : null}
    </div>
  );
};
