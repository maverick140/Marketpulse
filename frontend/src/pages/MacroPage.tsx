import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  Line,
} from 'recharts';
import {
  AlertCircle,
  Building2,
  Calendar,
  FileSpreadsheet,
  Globe2,
  RefreshCw,
  TrendingDown,
  TrendingUp,
  Percent,
} from 'lucide-react';
import { api } from '../api/client';
import { ProvenanceBadge } from '../components/ProvenanceBadge';
import { MacroDetail, MacroIndicator } from '../types';

export const MacroPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const indicatorParam = searchParams.get('indicator') || 'Real GDP Growth';

  const [indicators, setIndicators] = useState<MacroIndicator[]>([]);
  const [selectedName, setSelectedName] = useState(indicatorParam);
  const [detail, setDetail] = useState<MacroDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchIndicators = () => {
    setLoading(true);
    setError(null);
    api.getMacroList()
      .then((res) => {
        const list = res.indicators || [];
        setIndicators(list);
        if (list.length > 0) {
          const match = list.find((m) => m.indicator.toLowerCase() === indicatorParam.toLowerCase());
          if (match) {
            setSelectedName(match.indicator);
          } else if (!list.some((m) => m.indicator.toLowerCase() === selectedName.toLowerCase())) {
            setSelectedName(list[0].indicator);
          }
        }
      })
      .catch((err) => {
        console.error(err);
        setError('Failed to load macroeconomic indicators from backend.');
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchIndicators();
  }, []);

  useEffect(() => {
    setSelectedName(indicatorParam);
  }, [indicatorParam]);

  useEffect(() => {
    if (!selectedName) return;
    setLoading(true);
    setError(null);
    api.getMacroDetail(selectedName)
      .then((res) => {
        setDetail(res);
      })
      .catch((err) => {
        console.error(err);
        setError(`Unable to load historical records for ${selectedName}.`);
      })
      .finally(() => setLoading(false));
  }, [selectedName]);

  const handleSelect = (name: string) => {
    setSearchParams({ indicator: name });
    setSelectedName(name);
  };

  // Group into core official macro indicators vs secondary benchmarks
  const isPrimaryOfficial = (name: string) => {
    const n = name.toLowerCase();
    return n.includes('gdp') || n.includes('inflation') || n.includes('cpi') || n.includes('repo');
  };

  const primaryIndicators = indicators.filter((m) => isPrimaryOfficial(m.indicator));
  const secondaryBenchmarks = indicators.filter((m) => !isPrimaryOfficial(m.indicator));

  // Determine observation frequency / metadata
  const getFrequencyLabel = (indName: string) => {
    const n = indName.toLowerCase();
    if (n.includes('gdp')) return 'Quarterly YoY';
    if (n.includes('inflation') || n.includes('cpi')) return 'Monthly YoY';
    if (n.includes('repo') || n.includes('interest')) return 'Rate-Change Series';
    return 'Spot Benchmark';
  };

  const isStepChart = selectedName.toLowerCase().includes('repo') || selectedName.toLowerCase().includes('interest');

  const chartData = detail?.history.map((h) => ({
    period: h.period,
    value: h.value,
    date: h.date,
  })) || [];

  return (
    <div className="content-wrapper animate-fade">
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.25rem' }}>
            <h1 style={{ fontSize: '1.75rem', fontWeight: 800 }}>Macroeconomic Intelligence</h1>
            <ProvenanceBadge status={detail?.data_status || 'official'} />
          </div>
          <p style={{ color: '#94a3b8', fontSize: '0.875rem' }}>
            Systemic Indian macroeconomic metrics parsed directly from official Reserve Bank of India and MoSPI series workbooks.
          </p>
        </div>

        <button
          onClick={fetchIndicators}
          className="btn btn-secondary"
          style={{ fontSize: '0.8125rem', padding: '0.4rem 0.8rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}
        >
          <RefreshCw size={14} className={loading ? 'animate-spin' : ''} /> Refresh Indicators
        </button>
      </div>

      {/* Error state */}
      {error && (
        <div
          style={{
            backgroundColor: 'rgba(239, 68, 68, 0.1)',
            border: '1px solid rgba(239, 68, 68, 0.3)',
            borderRadius: '8px',
            padding: '1rem',
            marginBottom: '1.5rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            color: '#fca5a5',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <AlertCircle size={18} />
            <span style={{ fontSize: '0.875rem' }}>{error}</span>
          </div>
          <button onClick={fetchIndicators} className="btn btn-secondary" style={{ fontSize: '0.75rem', padding: '0.3rem 0.6rem' }}>
            Try Again
          </button>
        </div>
      )}

      {/* Section 1: Primary Official National Macro Indicators (GDP, CPI, Repo Rate) */}
      <div style={{ marginBottom: '1.75rem' }}>
        <h2 style={{ fontSize: '1rem', fontWeight: 700, color: '#f8fafc', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Building2 size={16} style={{ color: '#38bdf8' }} />
          India Official Macro Indicators
        </h2>

        <div className="grid-cols-3" style={{ gap: '1rem' }}>
          {primaryIndicators.map((m) => {
            const isSelected = m.indicator.toLowerCase() === selectedName.toLowerCase();
            const isPos = (m.change ?? 0) >= 0;
            const freq = getFrequencyLabel(m.indicator);
            return (
              <div
                key={m.indicator}
                onClick={() => handleSelect(m.indicator)}
                className="card card-hover"
                style={{
                  borderColor: isSelected ? '#38bdf8' : 'var(--border-color)',
                  backgroundColor: isSelected ? '#162032' : 'var(--bg-card)',
                  boxShadow: isSelected ? '0 0 15px rgba(56, 189, 248, 0.2)' : 'none',
                  cursor: 'pointer',
                  position: 'relative',
                  overflow: 'hidden',
                }}
              >
                {isSelected && (
                  <div
                    style={{
                      position: 'absolute',
                      top: 0,
                      left: 0,
                      right: 0,
                      height: '3px',
                      backgroundColor: '#38bdf8',
                    }}
                  />
                )}

                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                  <div>
                    <span style={{ fontSize: '0.875rem', color: '#f8fafc', fontWeight: 700 }}>
                      {m.indicator}
                    </span>
                    <span style={{ display: 'block', fontSize: '0.7rem', color: '#94a3b8' }}>
                      {freq}
                    </span>
                  </div>
                  <span className="badge badge-cached" style={{ fontSize: '0.65rem' }}>
                    {m.period}
                  </span>
                </div>

                <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.4rem', marginTop: '0.25rem' }}>
                  <span style={{ fontSize: '1.75rem', fontWeight: 800, fontFamily: 'var(--font-mono)' }}>
                    {m.value.toFixed(2)}
                  </span>
                  <span style={{ fontSize: '0.875rem', color: '#64748b', fontWeight: 600 }}>{m.unit}</span>

                  {m.change !== null && m.change !== 0 && (
                    <span
                      style={{
                        fontSize: '0.75rem',
                        fontWeight: 600,
                        color: isPos ? '#34d399' : '#f87171',
                        marginLeft: 'auto',
                        fontFamily: 'var(--font-mono)',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.15rem',
                      }}
                    >
                      {isPos ? <TrendingUp size={13} /> : <TrendingDown size={13} />}
                      {isPos ? '+' : ''}{m.change.toFixed(2)}
                    </span>
                  )}
                </div>

                <div style={{ marginTop: '0.75rem', paddingTop: '0.5rem', borderTop: '1px solid #1e293b', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                  <FileSpreadsheet size={13} style={{ color: '#10b981' }} />
                  <span style={{ fontSize: '0.6875rem', color: '#64748b', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {m.source}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Section 2: Selected Indicator Historical Trend Chart */}
      <div className="card" style={{ marginBottom: '1.75rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem', flexWrap: 'wrap', gap: '0.75rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.2rem' }}>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 800 }}>
                {detail?.current.indicator || selectedName} Historical Trend
              </h3>
              <span className="badge badge-cached" style={{ fontSize: '0.7rem' }}>
                {getFrequencyLabel(selectedName)}
              </span>
            </div>

            <p style={{ fontSize: '0.8125rem', color: '#94a3b8' }}>
              Latest: <strong style={{ color: '#f8fafc' }}>{detail?.current.value.toFixed(2)}{detail?.current.unit}</strong> ({detail?.current.period})
              {detail?.current.previous_value !== null && detail?.current.previous_value !== undefined && (
                <> • Prior: <span style={{ fontFamily: 'var(--font-mono)' }}>{detail.current.previous_value.toFixed(2)}{detail.current.unit}</span></>
              )}
              {detail?.current.change !== null && detail?.current.change !== undefined && (
                <> • Net Change: <span style={{ color: (detail.current.change >= 0 ? '#34d399' : '#f87171'), fontFamily: 'var(--font-mono)', fontWeight: 600 }}>
                  {detail.current.change >= 0 ? '+' : ''}{detail.current.change.toFixed(2)}{detail.current.unit}
                </span></>
              )}
            </p>
          </div>

          <div style={{ textAlign: 'right' }}>
            <ProvenanceBadge status={detail?.data_status || 'official'} provider={detail?.current.provider} />
            <p style={{ fontSize: '0.7rem', color: '#64748b', marginTop: '0.3rem', maxWidth: '320px' }}>
              {detail?.current.source}
            </p>
          </div>
        </div>

        {/* Historical Chart */}
        <div style={{ height: '340px', width: '100%', marginTop: '1rem' }}>
          {chartData.length === 0 ? (
            <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#64748b', fontSize: '0.875rem' }}>
              No historical observations available for {selectedName}
            </div>
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData} margin={{ top: 10, right: 30, left: 10, bottom: 20 }}>
                <defs>
                  <linearGradient id="macroGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#38bdf8" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#38bdf8" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis
                  dataKey="period"
                  stroke="#64748b"
                  fontSize={11}
                  tickLine={false}
                  angle={chartData.length > 15 ? -45 : 0}
                  textAnchor={chartData.length > 15 ? 'end' : 'middle'}
                  height={chartData.length > 15 ? 45 : 25}
                />
                <YAxis
                  stroke="#64748b"
                  domain={['auto', 'auto']}
                  fontSize={11}
                  orientation="right"
                  tickFormatter={(val) => `${val}${detail?.current.unit || '%'}`}
                />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }}
                  formatter={(val: any) => [`${Number(val).toFixed(2)}${detail?.current.unit || '%'}`, detail?.current.indicator || 'Value']}
                  labelFormatter={(lbl, items) => {
                    const rawDate = items && items[0] && (items[0].payload as any).date;
                    return rawDate ? `${lbl} (Date: ${rawDate})` : lbl;
                  }}
                />
                <Area
                  type={isStepChart ? 'stepAfter' : 'monotone'}
                  dataKey="value"
                  stroke="#38bdf8"
                  strokeWidth={2.5}
                  fillOpacity={1}
                  fill="url(#macroGrad)"
                />
              </AreaChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      {/* Section 3: Optional Commodity & FX Benchmark Spot Rates */}
      {secondaryBenchmarks.length > 0 && (
        <div>
          <h2 style={{ fontSize: '0.9375rem', fontWeight: 700, color: '#94a3b8', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <Globe2 size={15} style={{ color: '#f59e0b' }} />
            Global Commodity & Foreign Exchange Spot Rates
          </h2>

          <div className="grid-cols-3" style={{ gap: '1rem' }}>
            {secondaryBenchmarks.map((m) => {
              const isSelected = m.indicator.toLowerCase() === selectedName.toLowerCase();
              const isPos = (m.change ?? 0) >= 0;
              return (
                <div
                  key={m.indicator}
                  onClick={() => handleSelect(m.indicator)}
                  className="card card-hover"
                  style={{
                    borderColor: isSelected ? '#f59e0b' : 'var(--border-color)',
                    backgroundColor: isSelected ? '#162032' : 'var(--bg-card)',
                    cursor: 'pointer',
                    padding: '0.75rem 1rem',
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                    <span style={{ fontSize: '0.8125rem', color: '#cbd5e1', fontWeight: 600 }}>{m.indicator}</span>
                    <span className="badge badge-cached" style={{ fontSize: '0.65rem' }}>{m.period}</span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.4rem' }}>
                    <span style={{ fontSize: '1.25rem', fontWeight: 800, fontFamily: 'var(--font-mono)' }}>
                      {m.value.toFixed(2)}
                    </span>
                    <span style={{ fontSize: '0.75rem', color: '#64748b' }}>{m.unit}</span>
                    {m.change !== null && m.change !== 0 && (
                      <span style={{ fontSize: '0.75rem', fontWeight: 600, color: isPos ? '#34d399' : '#f87171', marginLeft: 'auto', fontFamily: 'var(--font-mono)' }}>
                        {isPos ? '+' : ''}{m.change.toFixed(2)}
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
