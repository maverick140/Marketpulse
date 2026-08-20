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
} from 'recharts';
import { Building2, Calendar, Globe2, TrendingDown, TrendingUp } from 'lucide-react';
import { api } from '../api/client';
import { ProvenanceBadge } from '../components/ProvenanceBadge';
import { MacroDetail, MacroIndicator } from '../types';

export const MacroPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const indicatorParam = searchParams.get('indicator') || 'Inflation';

  const [indicators, setIndicators] = useState<MacroIndicator[]>([]);
  const [selectedName, setSelectedName] = useState(indicatorParam);
  const [detail, setDetail] = useState<MacroDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setSelectedName(indicatorParam);
  }, [indicatorParam]);

  useEffect(() => {
    api.getMacroList()
      .then((res) => setIndicators(res.indicators || []))
      .catch(console.error);
  }, []);

  useEffect(() => {
    setLoading(true);
    api.getMacroDetail(selectedName)
      .then((res) => setDetail(res))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [selectedName]);

  const handleSelect = (name: string) => {
    setSearchParams({ indicator: name });
    setSelectedName(name);
  };

  const chartData = detail?.history.map((h) => ({
    period: h.period,
    value: h.value,
  })) || [];

  return (
    <div className="content-wrapper animate-fade">
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '1.5rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.25rem' }}>
            <h1 style={{ fontSize: '1.75rem', fontWeight: 800 }}>Macroeconomic Intelligence</h1>
            <ProvenanceBadge status={detail?.data_status || 'demo'} />
          </div>
          <p style={{ color: '#94a3b8', fontSize: '0.875rem' }}>
            Systemic macroeconomic surveillance covering inflation, policy rates, GDP, employment, and global commodity indices.
          </p>
        </div>
      </div>

      {/* Grid of 7 Macro Cards */}
      <div className="grid-cols-4" style={{ marginBottom: '1.5rem' }}>
        {indicators.map((m) => {
          const isSelected = m.indicator.toLowerCase() === selectedName.toLowerCase();
          const isPos = (m.change ?? 0) >= 0;
          return (
            <div
              key={m.indicator}
              onClick={() => handleSelect(m.indicator)}
              className="card card-hover"
              style={{
                borderColor: isSelected ? '#38bdf8' : 'var(--border-color)',
                backgroundColor: isSelected ? '#162032' : 'var(--bg-card)',
                boxShadow: isSelected ? '0 0 15px rgba(6, 182, 212, 0.2)' : 'none',
                cursor: 'pointer',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.4rem' }}>
                <span style={{ fontSize: '0.8125rem', color: '#94a3b8', fontWeight: 600 }}>{m.indicator}</span>
                <span className="badge badge-cached" style={{ fontSize: '0.65rem' }}>{m.period}</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.5rem' }}>
                <span style={{ fontSize: '1.5rem', fontWeight: 800, fontFamily: 'var(--font-mono)' }}>
                  {m.value}
                </span>
                <span style={{ fontSize: '0.75rem', color: '#64748b' }}>{m.unit}</span>
                {m.change !== null && m.change !== 0 && (
                  <span style={{ fontSize: '0.75rem', fontWeight: 600, color: isPos ? '#34d399' : '#f87171', marginLeft: 'auto', fontFamily: 'var(--font-mono)' }}>
                    {isPos ? '+' : ''}{m.change}
                  </span>
                )}
              </div>
              <p style={{ fontSize: '0.7rem', color: '#64748b', marginTop: '0.4rem' }}>Source: {m.source}</p>
            </div>
          );
        })}
      </div>

      {/* Detail Chart & Historical Series Card */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 800 }}>{detail?.current.indicator || selectedName} Historical Trend</h3>
            <p style={{ fontSize: '0.8125rem', color: '#94a3b8' }}>
              Latest: {detail?.current.value} {detail?.current.unit} (Period {detail?.current.period}) • Prior: {detail?.current.previous_value ?? '---'} {detail?.current.unit}
            </p>
          </div>
          <ProvenanceBadge status={detail?.data_status || 'demo'} provider={detail?.current.provider} />
        </div>

        {/* Historical Chart */}
        <div style={{ height: '320px', width: '100%', marginTop: '1rem' }}>
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id="macroGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="#f59e0b" stopOpacity={0.0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="period" stroke="#64748b" fontSize={11} />
              <YAxis stroke="#64748b" domain={['auto', 'auto']} fontSize={11} orientation="right" />
              <Tooltip
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }}
                formatter={(val: any) => [`${val} ${detail?.current.unit || ''}`, 'Value']}
              />
              <Area type="monotone" dataKey="value" stroke="#f59e0b" strokeWidth={2.5} fillOpacity={1} fill="url(#macroGrad)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
