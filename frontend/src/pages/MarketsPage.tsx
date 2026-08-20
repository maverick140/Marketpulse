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
import {
  Activity,
  Bookmark,
  Building2,
  Calendar,
  Check,
  LineChart,
  Plus,
  Search,
  TrendingDown,
  TrendingUp,
} from 'lucide-react';
import { api } from '../api/client';
import { ProvenanceBadge } from '../components/ProvenanceBadge';
import {
  MarketHistory,
  MarketOverview,
  MarketQuote,
  TechnicalIndicators,
} from '../types';

export const MarketsPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const symbolParam = searchParams.get('symbol') || 'RELIANCE';

  const [overview, setOverview] = useState<MarketOverview | null>(null);
  const [selectedSymbol, setSelectedSymbol] = useState(symbolParam);
  const [quote, setQuote] = useState<MarketQuote | null>(null);
  const [history, setHistory] = useState<MarketHistory | null>(null);
  const [indicators, setIndicators] = useState<TechnicalIndicators | null>(null);
  const [timeframe, setTimeframe] = useState('1M');
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[] | null>(null);
  const [isSearching, setIsSearching] = useState(false);
  const [inWatchlist, setInWatchlist] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setSelectedSymbol(symbolParam);
  }, [symbolParam]);

  useEffect(() => {
    api.getMarketOverview()
      .then((data) => setOverview(data))
      .catch(console.error);
  }, []);

  // Debounced dynamic search API call
  useEffect(() => {
    const q = searchQuery.trim();
    if (!q) {
      setSearchResults(null);
      setIsSearching(false);
      return;
    }

    setIsSearching(true);
    const timer = setTimeout(() => {
      api.searchMarkets(q)
        .then((res) => {
          setSearchResults(res.results || []);
        })
        .catch((err) => {
          console.error(err);
          setSearchResults([]);
        })
        .finally(() => {
          setIsSearching(false);
        });
    }, 300);

    return () => clearTimeout(timer);
  }, [searchQuery]);

  useEffect(() => {
    setLoading(true);
    Promise.allSettled([
      api.getQuote(selectedSymbol),
      api.getHistory(selectedSymbol, timeframe),
      api.getIndicators(selectedSymbol, timeframe),
      api.getWatchlist(),
    ]).then(([qRes, hRes, indRes, wRes]) => {
      if (qRes.status === 'fulfilled') setQuote(qRes.value);
      if (hRes.status === 'fulfilled') setHistory(hRes.value);
      if (indRes.status === 'fulfilled') setIndicators(indRes.value);
      if (wRes.status === 'fulfilled') {
        const found = wRes.value.items?.some((item: any) => item.symbol === selectedSymbol);
        setInWatchlist(Boolean(found));
      }
      setLoading(false);
    });
  }, [selectedSymbol, timeframe]);

  const handleSelectSymbol = (sym: string) => {
    setSearchParams({ symbol: sym });
    setSelectedSymbol(sym);
  };

  const toggleWatchlist = async () => {
    try {
      if (inWatchlist) {
        await api.removeFromWatchlist(selectedSymbol);
        setInWatchlist(false);
      } else {
        await api.addToWatchlist(selectedSymbol);
        setInWatchlist(true);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const allSecurities = [
    ...(overview?.gainers || []),
    ...(overview?.decliners || []),
    ...(overview?.most_active || []),
  ];
  // Deduplicate securities
  const uniqueSecurities = Array.from(new Map(allSecurities.map((s) => [s.symbol, s])).values());

  const chartData = history?.points.map((pt) => ({
    time: new Date(pt.timestamp).toLocaleDateString(undefined, { month: 'short', day: 'numeric' }),
    price: pt.close,
    open: pt.open,
    high: pt.high,
    low: pt.low,
    volume: pt.volume,
  })) || [];

  const isPos = (quote?.change_percent ?? 0) >= 0;

  return (
    <div className="content-wrapper animate-fade">
      <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: '1.5rem' }}>
        {/* Left Side: Securities Selector */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div className="card">
            <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <LineChart size={18} style={{ color: '#10b981' }} />
              Market Securities
            </h3>

            <div style={{ position: 'relative', marginBottom: '0.75rem' }}>
              <Search size={14} style={{ position: 'absolute', left: '10px', top: '12px', color: '#64748b' }} />
              <input
                type="text"
                className="input"
                placeholder="Search stocks, tickers & sectors..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                style={{ paddingLeft: '2rem', fontSize: '0.8125rem' }}
              />
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem', maxHeight: '520px', overflowY: 'auto' }}>
              {isSearching ? (
                <div style={{ textAlign: 'center', padding: '1.5rem 0.5rem', color: '#64748b' }}>
                  <p style={{ fontSize: '0.8125rem' }}>Searching markets...</p>
                </div>
              ) : searchResults !== null ? (
                searchResults.length === 0 ? (
                  <div style={{ textAlign: 'center', padding: '2rem 0.5rem', color: '#64748b' }}>
                    <p style={{ fontSize: '0.875rem', fontWeight: 600, color: '#94a3b8' }}>No stocks found</p>
                    <p style={{ fontSize: '0.75rem', marginTop: '0.25rem' }}>No securities matched "{searchQuery}"</p>
                  </div>
                ) : (
                  searchResults.map((sec) => (
                    <div
                      key={sec.symbol}
                      onClick={() => handleSelectSymbol(sec.symbol)}
                      className="card-hover"
                      style={{
                        padding: '0.55rem 0.75rem',
                        borderRadius: '8px',
                        backgroundColor: selectedSymbol === sec.symbol ? '#1e293b' : '#162032',
                        borderLeft: selectedSymbol === sec.symbol ? '3px solid #10b981' : '3px solid transparent',
                        cursor: 'pointer',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                      }}
                    >
                      <div>
                        <p style={{ fontSize: '0.8125rem', fontWeight: 700, color: '#f8fafc' }}>{sec.symbol}</p>
                        <p style={{ fontSize: '0.7rem', color: '#94a3b8', maxWidth: '160px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                          {sec.name}
                        </p>
                      </div>
                      <div style={{ textAlign: 'right', fontFamily: 'var(--font-mono)' }}>
                        {sec.price > 0 ? (
                          <>
                            <p style={{ fontSize: '0.8125rem', fontWeight: 700 }}>₹{sec.price.toFixed(2)}</p>
                            <p style={{ fontSize: '0.7rem', color: (sec.change_percent ?? 0) >= 0 ? '#34d399' : '#f87171' }}>
                              {(sec.change_percent ?? 0) >= 0 ? '+' : ''}{sec.change_percent?.toFixed(2)}%
                            </p>
                          </>
                        ) : (
                          <span className="badge badge-cached" style={{ fontSize: '0.65rem' }}>{sec.sector || 'EQUITY'}</span>
                        )}
                      </div>
                    </div>
                  ))
                )
              ) : (
                <>
                  {/* Default Indices */}
                  {overview?.indices.map((idx) => (
                    <div
                      key={idx.symbol}
                      onClick={() => handleSelectSymbol(idx.symbol)}
                      className="card-hover"
                      style={{
                        padding: '0.55rem 0.75rem',
                        borderRadius: '8px',
                        backgroundColor: selectedSymbol === idx.symbol ? '#1e293b' : '#162032',
                        borderLeft: selectedSymbol === idx.symbol ? '3px solid #10b981' : '3px solid transparent',
                        cursor: 'pointer',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                      }}
                    >
                      <div>
                        <p style={{ fontSize: '0.8125rem', fontWeight: 700 }}>{idx.symbol}</p>
                        <span className="badge badge-cached" style={{ fontSize: '0.65rem', padding: '0.1rem 0.35rem' }}>INDEX</span>
                      </div>
                      <div style={{ textAlign: 'right', fontFamily: 'var(--font-mono)' }}>
                        <p style={{ fontSize: '0.8125rem', fontWeight: 700 }}>{idx.value.toLocaleString()}</p>
                        <p style={{ fontSize: '0.7rem', color: (idx.change_percent ?? 0) >= 0 ? '#34d399' : '#f87171' }}>
                          {(idx.change_percent ?? 0) >= 0 ? '+' : ''}{idx.change_percent?.toFixed(2)}%
                        </p>
                      </div>
                    </div>
                  ))}

                  {/* Default Equities */}
                  {uniqueSecurities.map((sec) => (
                    <div
                      key={sec.symbol}
                      onClick={() => handleSelectSymbol(sec.symbol)}
                      className="card-hover"
                      style={{
                        padding: '0.55rem 0.75rem',
                        borderRadius: '8px',
                        backgroundColor: selectedSymbol === sec.symbol ? '#1e293b' : '#162032',
                        borderLeft: selectedSymbol === sec.symbol ? '3px solid #10b981' : '3px solid transparent',
                        cursor: 'pointer',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                      }}
                    >
                      <div>
                        <p style={{ fontSize: '0.8125rem', fontWeight: 700 }}>{sec.symbol}</p>
                        <p style={{ fontSize: '0.7rem', color: '#94a3b8' }}>{sec.sector || 'Equities'}</p>
                      </div>
                      <div style={{ textAlign: 'right', fontFamily: 'var(--font-mono)' }}>
                        <p style={{ fontSize: '0.8125rem', fontWeight: 700 }}>₹{sec.price.toFixed(2)}</p>
                        <p style={{ fontSize: '0.7rem', color: (sec.change_percent ?? 0) >= 0 ? '#34d399' : '#f87171' }}>
                          {(sec.change_percent ?? 0) >= 0 ? '+' : ''}{sec.change_percent?.toFixed(2)}%
                        </p>
                      </div>
                    </div>
                  ))}
                </>
              )}
            </div>
          </div>
        </div>

        {/* Right Side: Security Detail & Charts */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          {/* Quote Header Card */}
          <div className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.2rem' }}>
                  <h2 style={{ fontSize: '1.5rem', fontWeight: 800 }}>{quote?.symbol || selectedSymbol}</h2>
                  <ProvenanceBadge status={quote?.data_status || 'demo'} provider={quote?.provider} />
                  {quote?.sector && <span className="badge badge-cached">{quote.sector}</span>}
                </div>
                <p style={{ color: '#94a3b8', fontSize: '0.85rem' }}>{quote?.name || 'Security Intelligence Overview'}</p>
              </div>

              <button
                onClick={toggleWatchlist}
                className={`btn ${inWatchlist ? 'btn-secondary' : 'btn-primary'}`}
                style={{ fontSize: '0.8125rem', padding: '0.4rem 0.85rem' }}
              >
                {inWatchlist ? <Check size={14} /> : <Plus size={14} />}
                {inWatchlist ? 'In Watchlist' : 'Add to Watchlist'}
              </button>
            </div>

            {/* Price Ribbon */}
            <div style={{ display: 'flex', alignItems: 'baseline', gap: '1.25rem', marginTop: '1rem', paddingBottom: '0.5rem', borderBottom: '1px solid #1e293b' }}>
              <span style={{ fontSize: '2.25rem', fontWeight: 800, fontFamily: 'var(--font-mono)' }}>
                ₹{quote?.price ? quote.price.toFixed(2) : '---'}
              </span>

              {quote?.change_percent !== null && quote?.change_percent !== undefined && (
                <span
                  style={{
                    fontSize: '1.125rem',
                    fontWeight: 700,
                    fontFamily: 'var(--font-mono)',
                    color: isPos ? '#34d399' : '#f87171',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.3rem',
                  }}
                >
                  {isPos ? <TrendingUp size={20} /> : <TrendingDown size={20} />}
                  {isPos ? '+' : ''}{quote.change_percent.toFixed(2)}% ({quote.change ? (isPos ? '+' : '') + quote.change.toFixed(2) : ''})
                </span>
              )}

              {quote?.volume && (
                <span style={{ fontSize: '0.8125rem', color: '#94a3b8', marginLeft: 'auto', fontFamily: 'var(--font-mono)' }}>
                  Volume: {quote.volume.toLocaleString()}
                </span>
              )}
            </div>

            {/* Timeframe selector */}
            <div style={{ display: 'flex', gap: '0.4rem', marginTop: '1rem' }}>
              {['1D', '5D', '1M', '3M', '6M', '1Y'].map((tf) => (
                <button
                  key={tf}
                  onClick={() => setTimeframe(tf)}
                  style={{
                    background: timeframe === tf ? '#10b981' : '#1e293b',
                    color: timeframe === tf ? '#0b0f17' : '#cbd5e1',
                    fontWeight: 700,
                    fontSize: '0.75rem',
                    border: 'none',
                    padding: '0.35rem 0.75rem',
                    borderRadius: '6px',
                    cursor: 'pointer',
                  }}
                >
                  {tf}
                </button>
              ))}
            </div>

            {/* Price Chart */}
            <div style={{ height: '320px', marginTop: '1rem', width: '100%' }}>
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData}>
                  <defs>
                    <linearGradient id="priceGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor={isPos ? '#10b981' : '#f43f5e'} stopOpacity={0.4} />
                      <stop offset="95%" stopColor={isPos ? '#10b981' : '#f43f5e'} stopOpacity={0.0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="time" stroke="#64748b" fontSize={11} />
                  <YAxis stroke="#64748b" domain={['auto', 'auto']} fontSize={11} orientation="right" />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }}
                    formatter={(val: any) => [`₹${Number(val).toFixed(2)}`, 'Price']}
                  />
                  <Area
                    type="monotone"
                    dataKey="price"
                    stroke={isPos ? '#10b981' : '#f43f5e'}
                    strokeWidth={2}
                    fillOpacity={1}
                    fill="url(#priceGrad)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Technical Indicators Analytics Grid */}
          <div className="card">
            <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Activity size={18} style={{ color: '#06b6d4' }} />
              Educational Technical Indicators ({timeframe})
            </h3>

            <div className="grid-cols-4">
              <div style={{ backgroundColor: '#162032', padding: '0.75rem', borderRadius: '8px' }}>
                <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>SMA (20-period)</span>
                <p style={{ fontSize: '1.125rem', fontWeight: 700, fontFamily: 'var(--font-mono)', marginTop: '0.2rem' }}>
                  {indicators?.sma_20 ? `₹${indicators.sma_20.toFixed(2)}` : '---'}
                </p>
              </div>

              <div style={{ backgroundColor: '#162032', padding: '0.75rem', borderRadius: '8px' }}>
                <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>EMA (20-period)</span>
                <p style={{ fontSize: '1.125rem', fontWeight: 700, fontFamily: 'var(--font-mono)', marginTop: '0.2rem' }}>
                  {indicators?.ema_20 ? `₹${indicators.ema_20.toFixed(2)}` : '---'}
                </p>
              </div>

              <div style={{ backgroundColor: '#162032', padding: '0.75rem', borderRadius: '8px' }}>
                <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>RSI (14-period)</span>
                <p style={{ fontSize: '1.125rem', fontWeight: 700, fontFamily: 'var(--font-mono)', marginTop: '0.2rem', color: (indicators?.rsi_14 ?? 50) > 70 ? '#f87171' : (indicators?.rsi_14 ?? 50) < 30 ? '#34d399' : '#38bdf8' }}>
                  {indicators?.rsi_14 ? indicators.rsi_14.toFixed(1) : '---'}
                </p>
              </div>

              <div style={{ backgroundColor: '#162032', padding: '0.75rem', borderRadius: '8px' }}>
                <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Annualized Volatility</span>
                <p style={{ fontSize: '1.125rem', fontWeight: 700, fontFamily: 'var(--font-mono)', marginTop: '0.2rem' }}>
                  {indicators?.volatility ? `${indicators.volatility.toFixed(1)}%` : '---'}
                </p>
              </div>
            </div>

            <div style={{ marginTop: '0.85rem', padding: '0.65rem 0.85rem', backgroundColor: '#0b0f17', borderRadius: '6px', border: '1px solid #1e293b', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                MACD (12/26/9): Line <strong>{indicators?.macd.macd_line ?? '0.00'}</strong> | Signal <strong>{indicators?.macd.signal_line ?? '0.00'}</strong> | Hist <strong>{indicators?.macd.histogram ?? '0.00'}</strong>
              </span>
              <span style={{ fontSize: '0.72rem', color: '#64748b' }}>{indicators?.disclaimer}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
