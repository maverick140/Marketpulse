import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  AlertCircle,
  Building2,
  Calendar,
  Globe2,
  LineChart,
  Newspaper,
  Search,
  TrendingUp,
  X,
} from 'lucide-react';
import { api } from '../api/client';

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export const GlobalSearchModal: React.FC<Props> = ({ isOpen, onClose }) => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!isOpen) {
      setQuery('');
      setResults(null);
      return;
    }

    const timer = setTimeout(async () => {
      if (query.trim()) {
        setLoading(true);
        try {
          const res = await api.unifiedSearch(query);
          setResults(res);
        } catch (e) {
          console.error(e);
        } finally {
          setLoading(false);
        }
      } else {
        setResults(null);
      }
    }, 200);

    return () => clearTimeout(timer);
  }, [query, isOpen]);

  if (!isOpen) return null;

  const handleSelect = (category: string, identifier: string) => {
    onClose();
    if (category === 'Markets') {
      navigate(`/markets?symbol=${identifier}`);
    } else if (category === 'Macro') {
      navigate(`/macro?indicator=${identifier}`);
    } else if (category === 'News') {
      navigate(`/news?q=${identifier}`);
    } else if (category === 'Geopolitics') {
      navigate(`/geopolitics?id=${identifier}`);
    } else if (category === 'Announcements') {
      navigate(`/announcements`);
    }
  };

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(5, 8, 15, 0.85)',
        backdropFilter: 'blur(8px)',
        display: 'flex',
        alignItems: 'flex-start',
        justifyContent: 'center',
        zIndex: 9999,
        paddingTop: '10vh',
        paddingLeft: '1rem',
        paddingRight: '1rem',
      }}
      onClick={onClose}
    >
      <div
        className="card animate-fade"
        style={{
          maxWidth: '680px',
          width: '100%',
          backgroundColor: '#0f172a',
          borderColor: '#1e293b',
          padding: '1.25rem',
          maxHeight: '75vh',
          display: 'flex',
          flexDirection: 'column',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Search Bar Input */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', paddingBottom: '1rem', borderBottom: '1px solid #1e293b' }}>
          <Search size={20} style={{ color: '#38bdf8' }} />
          <input
            autoFocus
            type="text"
            className="input"
            placeholder="Search equities, macro indicators, news, geopolitics..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            style={{ fontSize: '1rem', padding: '0.5rem', background: 'transparent', border: 'none', boxShadow: 'none' }}
          />
          {query && (
            <button onClick={() => setQuery('')} style={{ background: 'none', border: 'none', color: '#64748b', cursor: 'pointer' }}>
              <X size={18} />
            </button>
          )}
          <span style={{ fontSize: '0.75rem', color: '#64748b', border: '1px solid #1e293b', padding: '0.2rem 0.4rem', borderRadius: '4px' }}>
            ESC
          </span>
        </div>

        {/* Search Results Display */}
        <div style={{ overflowY: 'auto', flex: 1, marginTop: '1rem' }}>
          {loading && (
            <div style={{ padding: '2rem', textAlign: 'center', color: '#64748b', fontSize: '0.875rem' }}>
              Searching across MarketPulse intelligence domains...
            </div>
          )}

          {!loading && results && results.total_results === 0 && (
            <div style={{ padding: '2rem', textAlign: 'center', color: '#64748b', fontSize: '0.875rem' }}>
              No intelligence records found matching "{query}".
            </div>
          )}

          {!loading && !results && !query && (
            <div style={{ padding: '1.5rem', color: '#64748b', fontSize: '0.8125rem' }}>
              <p style={{ fontWeight: 600, color: '#94a3b8', marginBottom: '0.5rem' }}>SUGGESTIONS</p>
              <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                {['RELIANCE', 'INFY', 'TCS', 'Inflation', 'Crude Oil', 'Technology', 'SEBI'].map((tag) => (
                  <button
                    key={tag}
                    onClick={() => setQuery(tag)}
                    style={{
                      background: '#1e293b',
                      border: '1px solid #334155',
                      color: '#cbd5e1',
                      padding: '0.25rem 0.6rem',
                      borderRadius: '6px',
                      fontSize: '0.75rem',
                      cursor: 'pointer',
                    }}
                  >
                    {tag}
                  </button>
                ))}
              </div>
            </div>
          )}

          {results && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {/* Markets */}
              {results.markets?.length > 0 && (
                <div>
                  <p style={{ fontSize: '0.75rem', fontWeight: 700, color: '#38bdf8', marginBottom: '0.4rem', textTransform: 'uppercase' }}>
                    Markets & Equities ({results.markets.length})
                  </p>
                  {results.markets.map((item: any, i: number) => (
                    <div
                      key={i}
                      onClick={() => handleSelect('Markets', item.identifier)}
                      className="card-hover"
                      style={{ padding: '0.6rem 0.75rem', borderRadius: '8px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.6rem' }}
                    >
                      <LineChart size={16} style={{ color: '#34d399' }} />
                      <div style={{ flex: 1 }}>
                        <p style={{ fontSize: '0.875rem', fontWeight: 600, color: '#f8fafc' }}>{item.title}</p>
                        <p style={{ fontSize: '0.75rem', color: '#94a3b8' }}>{item.subtitle}</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Macro */}
              {results.macro?.length > 0 && (
                <div>
                  <p style={{ fontSize: '0.75rem', fontWeight: 700, color: '#f59e0b', marginBottom: '0.4rem', textTransform: 'uppercase' }}>
                    Macro Indicators ({results.macro.length})
                  </p>
                  {results.macro.map((item: any, i: number) => (
                    <div
                      key={i}
                      onClick={() => handleSelect('Macro', item.identifier)}
                      className="card-hover"
                      style={{ padding: '0.6rem 0.75rem', borderRadius: '8px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.6rem' }}
                    >
                      <Building2 size={16} style={{ color: '#f59e0b' }} />
                      <div style={{ flex: 1 }}>
                        <p style={{ fontSize: '0.875rem', fontWeight: 600, color: '#f8fafc' }}>{item.title}</p>
                        <p style={{ fontSize: '0.75rem', color: '#94a3b8' }}>{item.subtitle}</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* News */}
              {results.news?.length > 0 && (
                <div>
                  <p style={{ fontSize: '0.75rem', fontWeight: 700, color: '#a855f7', marginBottom: '0.4rem', textTransform: 'uppercase' }}>
                    News Articles ({results.news.length})
                  </p>
                  {results.news.map((item: any, i: number) => (
                    <div
                      key={i}
                      onClick={() => handleSelect('News', item.identifier)}
                      className="card-hover"
                      style={{ padding: '0.6rem 0.75rem', borderRadius: '8px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.6rem' }}
                    >
                      <Newspaper size={16} style={{ color: '#c084fc' }} />
                      <div style={{ flex: 1 }}>
                        <p style={{ fontSize: '0.875rem', fontWeight: 600, color: '#f8fafc' }}>{item.title}</p>
                        <p style={{ fontSize: '0.75rem', color: '#94a3b8' }}>{item.subtitle}</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Geopolitics */}
              {results.geopolitics?.length > 0 && (
                <div>
                  <p style={{ fontSize: '0.75rem', fontWeight: 700, color: '#f43f5e', marginBottom: '0.4rem', textTransform: 'uppercase' }}>
                    Geopolitical Events ({results.geopolitics.length})
                  </p>
                  {results.geopolitics.map((item: any, i: number) => (
                    <div
                      key={i}
                      onClick={() => handleSelect('Geopolitics', item.identifier)}
                      className="card-hover"
                      style={{ padding: '0.6rem 0.75rem', borderRadius: '8px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.6rem' }}
                    >
                      <Globe2 size={16} style={{ color: '#fb7185' }} />
                      <div style={{ flex: 1 }}>
                        <p style={{ fontSize: '0.875rem', fontWeight: 600, color: '#f8fafc' }}>{item.title}</p>
                        <p style={{ fontSize: '0.75rem', color: '#94a3b8' }}>{item.subtitle}</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
