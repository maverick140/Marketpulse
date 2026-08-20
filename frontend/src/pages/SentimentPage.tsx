import React, { useEffect, useState } from 'react';
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { Cpu, Flame, Play, Sparkles, TrendingUp } from 'lucide-react';
import { api } from '../api/client';
import { MetricCard } from '../components/MetricCard';
import { ProvenanceBadge } from '../components/ProvenanceBadge';
import { SentimentAnalysis } from '../types';

export const SentimentPage: React.FC = () => {
  const [sentiment, setSentiment] = useState<SentimentAnalysis | null>(null);
  const [trends, setTrends] = useState<any[]>([]);
  const [timeframe, setTimeframe] = useState('7D');
  const [testText, setTestText] = useState('Infosys beats quarterly forecasts with strong cloud margin expansion.');
  const [customResult, setCustomResult] = useState<any>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    Promise.allSettled([
      api.getMarketSentiment(),
      api.getSentimentTrends(timeframe),
    ]).then(([sRes, tRes]) => {
      if (sRes.status === 'fulfilled') setSentiment(sRes.value);
      if (tRes.status === 'fulfilled') setTrends(tRes.value.trends || []);
      setLoading(false);
    });
  }, [timeframe]);

  const handleAnalyzeCustom = async () => {
    if (!testText.trim()) return;
    setAnalyzing(true);
    try {
      const res = await api.analyzeText(testText);
      setCustomResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setAnalyzing(false);
    }
  };

  const distData = [
    { name: 'Positive', count: sentiment?.distribution.positive ?? 0, color: '#10b981' },
    { name: 'Neutral', count: sentiment?.distribution.neutral ?? 0, color: '#64748b' },
    { name: 'Negative', count: sentiment?.distribution.negative ?? 0, color: '#f43f5e' },
  ];

  return (
    <div className="content-wrapper animate-fade">
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '1.5rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.25rem' }}>
            <h1 style={{ fontSize: '1.75rem', fontWeight: 800 }}>Sentiment Intelligence Engine</h1>
            <span className="badge badge-positive">FINANCIAL LEXICON NLP</span>
          </div>
          <p style={{ color: '#94a3b8', fontSize: '0.875rem' }}>
            Explainable NLP scoring, entity sentiment aggregation, sectoral heatmaps, and custom text simulation.
          </p>
        </div>
      </div>

      {/* Top Metrics Ribbon */}
      <div className="grid-cols-4" style={{ marginBottom: '1.5rem' }}>
        <MetricCard
          title="Overall Market Score"
          value={sentiment ? `${sentiment.overall_score > 0 ? '+' : ''}${sentiment.overall_score.toFixed(2)}` : '0.00'}
          badge={<span className="badge badge-positive">{sentiment?.overall_label.toUpperCase()}</span>}
          subtitle="Scale: -1.0 (Bearish) to +1.0 (Bullish)"
          icon={<Flame size={16} />}
        />
        <MetricCard
          title="Confidence Rating"
          value={sentiment ? `${(sentiment.confidence * 100).toFixed(0)}%` : '0%'}
          badge={<span className="badge badge-cached">MODEL v1.0</span>}
          subtitle="Token density & negation coverage"
        />
        <MetricCard
          title="Articles Synthesized"
          value={sentiment?.total_articles ?? 0}
          subtitle="Financial news corpus coverage"
        />
        <MetricCard
          title="Positive vs Negative Ratio"
          value={`${sentiment?.distribution.positive ?? 0} : ${sentiment?.distribution.negative ?? 0}`}
          subtitle="Positive / Negative distribution"
        />
      </div>

      {/* Main Two Column: Sector Breakdown & Historical Trends */}
      <div className="grid-cols-2" style={{ marginBottom: '1.5rem' }}>
        {/* Left: Sector Breakdown */}
        <div className="card">
          <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Flame size={18} style={{ color: '#f59e0b' }} />
            Sectoral Sentiment Breakdown
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
            {sentiment?.sectors.map((sec) => (
              <div
                key={sec.sector}
                style={{
                  backgroundColor: '#162032',
                  padding: '0.75rem 1rem',
                  borderRadius: '8px',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <div>
                  <p style={{ fontSize: '0.875rem', fontWeight: 700 }}>{sec.sector}</p>
                  <p style={{ fontSize: '0.72rem', color: '#94a3b8' }}>{sec.article_count} articles tracked</p>
                </div>
                <div style={{ textAlign: 'right', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                  <span
                    style={{
                      fontFamily: 'var(--font-mono)',
                      fontSize: '0.875rem',
                      fontWeight: 700,
                      color: sec.average_score > 0 ? '#34d399' : sec.average_score < 0 ? '#f87171' : '#cbd5e1',
                    }}
                  >
                    {sec.average_score > 0 ? '+' : ''}{sec.average_score.toFixed(2)}
                  </span>
                  <span className={`badge ${sec.label === 'positive' ? 'badge-positive' : sec.label === 'negative' ? 'badge-negative' : 'badge-neutral'}`}>
                    {sec.label}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right: Trend Chart */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h3 style={{ fontSize: '1rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <TrendingUp size={18} style={{ color: '#10b981' }} />
              Sentiment Trajectory ({timeframe})
            </h3>
            <div style={{ display: 'flex', gap: '0.3rem' }}>
              {['7D', '30D'].map((tf) => (
                <button
                  key={tf}
                  onClick={() => setTimeframe(tf)}
                  style={{
                    backgroundColor: timeframe === tf ? '#10b981' : '#1e293b',
                    color: timeframe === tf ? '#0b0f17' : '#cbd5e1',
                    border: 'none',
                    padding: '0.25rem 0.6rem',
                    borderRadius: '4px',
                    fontSize: '0.72rem',
                    fontWeight: 700,
                    cursor: 'pointer',
                  }}
                >
                  {tf}
                </button>
              ))}
            </div>
          </div>

          <div style={{ height: '280px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trends}>
                <defs>
                  <linearGradient id="sentGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="date" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" domain={[-1, 1]} fontSize={11} orientation="right" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }}
                  formatter={(val: any) => [`${Number(val) > 0 ? '+' : ''}${Number(val).toFixed(2)}`, 'Sentiment Score']}
                />
                <Area type="monotone" dataKey="score" stroke="#10b981" strokeWidth={2} fillOpacity={1} fill="url(#sentGrad)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Interactive Text Sentiment Sandbox */}
      <div className="card" style={{ borderColor: 'rgba(139, 92, 246, 0.3)' }}>
        <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.6rem', color: '#c084fc', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Sparkles size={18} />
          Interactive Sentiment Analysis Sandbox
        </h3>
        <p style={{ fontSize: '0.8125rem', color: '#94a3b8', marginBottom: '0.85rem' }}>
          Test arbitrary financial headlines, earnings quotes, or policy commentary through our explainable NLP scoring pipeline.
        </p>

        <div style={{ display: 'flex', gap: '0.75rem', marginBottom: '1rem' }}>
          <input
            type="text"
            className="input"
            value={testText}
            onChange={(e) => setTestText(e.target.value)}
            placeholder="Type or paste financial headline..."
            style={{ fontSize: '0.875rem' }}
          />
          <button onClick={handleAnalyzeCustom} disabled={analyzing} className="btn btn-primary" style={{ whiteSpace: 'nowrap' }}>
            <Play size={14} />
            {analyzing ? 'Scoring...' : 'Analyze Text'}
          </button>
        </div>

        {customResult && (
          <div className="animate-fade" style={{ backgroundColor: '#0b0f17', padding: '1rem', borderRadius: '8px', border: '1px solid #1e293b', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
            <div>
              <span style={{ fontSize: '0.75rem', color: '#64748b' }}>CLASSIFICATION</span>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginTop: '0.2rem' }}>
                <span className={`badge ${customResult.label === 'positive' ? 'badge-positive' : customResult.label === 'negative' ? 'badge-negative' : 'badge-neutral'}`} style={{ fontSize: '0.85rem', padding: '0.3rem 0.75rem' }}>
                  {customResult.label.toUpperCase()}
                </span>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '1.25rem', fontWeight: 800, color: customResult.score > 0 ? '#34d399' : customResult.score < 0 ? '#f87171' : '#cbd5e1' }}>
                  {customResult.score > 0 ? '+' : ''}{customResult.score.toFixed(2)}
                </span>
              </div>
            </div>

            <div>
              <span style={{ fontSize: '0.75rem', color: '#64748b' }}>CONFIDENCE</span>
              <p style={{ fontSize: '1.125rem', fontWeight: 700, fontFamily: 'var(--font-mono)', color: '#38bdf8' }}>
                {(customResult.confidence * 100).toFixed(0)}%
              </p>
            </div>

            <div>
              <span style={{ fontSize: '0.75rem', color: '#64748b' }}>TOKENS DETECTED</span>
              <p style={{ fontSize: '0.875rem', color: '#94a3b8' }}>
                +{customResult.positive_count} pos / -{customResult.negative_count} neg ({customResult.total_tokens} words)
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
