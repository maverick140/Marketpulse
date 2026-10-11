import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Bookmark,
  Check,
  FileText,
  LineChart,
  Plus,
  Settings,
  Trash2,
} from 'lucide-react';
import { api } from '../api/client';

export const WorkspacePage: React.FC = () => {
  const [watchlist, setWatchlist] = useState<any[]>([]);
  const [research, setResearch] = useState<any[]>([]);
  const [newSymbol, setNewSymbol] = useState('');
  const [preferences, setPreferences] = useState({
    theme: 'dark',
    default_timeframe: '1M',
    disclaimer_acknowledged: true,
    alert_notifications_enabled: true,
  });
  const [activeTab, setActiveTab] = useState<'watchlist' | 'research' | 'preferences'>('watchlist');
  const navigate = useNavigate();

  const loadData = () => {
    Promise.allSettled([
      api.getWatchlist(),
      api.getSavedResearch(),
      api.getPreferences(),
    ]).then(([wRes, rRes, pRes]) => {
      if (wRes.status === 'fulfilled') setWatchlist(wRes.value.items || []);
      if (rRes.status === 'fulfilled') setResearch(rRes.value.items || []);
      if (pRes.status === 'fulfilled') setPreferences(pRes.value);
    });
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleAddSymbol = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newSymbol.trim()) return;
    try {
      await api.addToWatchlist(newSymbol.trim().toUpperCase());
      setNewSymbol('');
      loadData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleRemoveWatchlist = async (sym: string) => {
    try {
      await api.removeFromWatchlist(sym);
      loadData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteResearch = async (id: string) => {
    try {
      await api.deleteSavedResearch(id);
      loadData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleSavePreferences = async (newTf: string) => {
    try {
      const updated = { ...preferences, default_timeframe: newTf };
      await api.updatePreferences(updated);
      setPreferences(updated);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="content-wrapper animate-fade">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '1.5rem' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 800 }}>Research Workspace</h1>
          <p style={{ color: '#94a3b8', fontSize: '0.875rem' }}>
            Personal intelligence workspace, tracked equities watchlist, saved AI synthesis notes, and platform preferences.
          </p>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem', borderBottom: '1px solid #1e293b', paddingBottom: '0.5rem' }}>
        <button
          onClick={() => setActiveTab('watchlist')}
          style={{
            background: 'none',
            border: 'none',
            color: activeTab === 'watchlist' ? '#10b981' : '#94a3b8',
            fontSize: '0.875rem',
            fontWeight: 700,
            cursor: 'pointer',
            padding: '0.5rem 0.75rem',
            borderBottom: activeTab === 'watchlist' ? '2px solid #10b981' : '2px solid transparent',
          }}
        >
          Tracked Watchlist ({watchlist.length})
        </button>

        <button
          onClick={() => setActiveTab('research')}
          style={{
            background: 'none',
            border: 'none',
            color: activeTab === 'research' ? '#10b981' : '#94a3b8',
            fontSize: '0.875rem',
            fontWeight: 700,
            cursor: 'pointer',
            padding: '0.5rem 0.75rem',
            borderBottom: activeTab === 'research' ? '2px solid #10b981' : '2px solid transparent',
          }}
        >
          Saved AI Notes ({research.length})
        </button>

        <button
          onClick={() => setActiveTab('preferences')}
          style={{
            background: 'none',
            border: 'none',
            color: activeTab === 'preferences' ? '#10b981' : '#94a3b8',
            fontSize: '0.875rem',
            fontWeight: 700,
            cursor: 'pointer',
            padding: '0.5rem 0.75rem',
            borderBottom: activeTab === 'preferences' ? '2px solid #10b981' : '2px solid transparent',
          }}
        >
          Preferences
        </button>
      </div>

      {/* Watchlist Tab View */}
      {activeTab === 'watchlist' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <form onSubmit={handleAddSymbol} style={{ display: 'flex', gap: '0.75rem', maxWidth: '400px' }}>
            <input
              type="text"
              className="input"
              placeholder="Add ticker symbol (e.g. SBIN)..."
              value={newSymbol}
              onChange={(e) => setNewSymbol(e.target.value)}
            />
            <button type="submit" className="btn btn-primary" style={{ whiteSpace: 'nowrap' }}>
              <Plus size={15} /> Add Symbol
            </button>
          </form>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
            {watchlist.map((item) => (
              <div key={item.symbol} className="card card-hover" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <h4 style={{ fontSize: '1.125rem', fontWeight: 800 }}>{item.symbol}</h4>
                  <p style={{ fontSize: '0.75rem', color: '#94a3b8' }}>{item.name || `${item.symbol} (demo)`}</p>
                </div>
                <div style={{ display: 'flex', gap: '0.4rem' }}>
                  <button
                    onClick={() => navigate(`/markets?symbol=${item.symbol}`)}
                    className="btn btn-secondary"
                    style={{ padding: '0.35rem 0.6rem', fontSize: '0.75rem' }}
                  >
                    <LineChart size={14} /> Open
                  </button>
                  <button
                    onClick={() => handleRemoveWatchlist(item.symbol)}
                    style={{ background: 'none', border: 'none', color: '#64748b', cursor: 'pointer', padding: '0.35rem' }}
                    title="Remove from watchlist"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Saved Research Tab View */}
      {activeTab === 'research' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {research.length === 0 ? (
            <div className="card" style={{ padding: '2rem', textAlign: 'center', color: '#64748b' }}>
              <Bookmark size={32} style={{ margin: '0 auto 0.5rem auto', opacity: 0.5 }} />
              <p>No saved research notes yet. Click "Save Research" in the AI Analyst view to store notes here.</p>
            </div>
          ) : (
            research.map((item) => (
              <div key={item.id} className="card card-hover">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.4rem' }}>
                  <div>
                    <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: '#f8fafc' }}>{item.title}</h3>
                    <p style={{ fontSize: '0.75rem', color: '#64748b', fontFamily: 'var(--font-mono)' }}>
                      Query: {item.query}
                    </p>
                  </div>
                  <button
                    onClick={() => handleDeleteResearch(item.id)}
                    style={{ background: 'none', border: 'none', color: '#64748b', cursor: 'pointer' }}
                  >
                    <Trash2 size={16} />
                  </button>
                </div>

                <p style={{ fontSize: '0.875rem', color: '#cbd5e1', lineHeight: 1.6, marginBottom: '0.75rem' }}>
                  {item.summary}
                </p>

                <div style={{ display: 'flex', gap: '0.4rem' }}>
                  {item.tags?.map((t: string) => (
                    <span key={t} className="badge badge-cached">{t}</span>
                  ))}
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* Preferences Tab View */}
      {activeTab === 'preferences' && (
        <div className="card" style={{ maxWidth: '600px' }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '1rem' }}>Platform Preferences</h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            <div>
              <label style={{ fontSize: '0.8125rem', color: '#94a3b8', fontWeight: 600, display: 'block', marginBottom: '0.4rem' }}>
                DEFAULT MARKET TIMEFRAME
              </label>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                {['1D', '1M', '3M', '1Y'].map((tf) => (
                  <button
                    key={tf}
                    onClick={() => handleSavePreferences(tf)}
                    style={{
                      backgroundColor: preferences.default_timeframe === tf ? '#10b981' : '#1e293b',
                      color: preferences.default_timeframe === tf ? '#0b0f17' : '#cbd5e1',
                      border: 'none',
                      padding: '0.4rem 0.8rem',
                      borderRadius: '6px',
                      fontSize: '0.8125rem',
                      fontWeight: 700,
                      cursor: 'pointer',
                    }}
                  >
                    {tf}
                  </button>
                ))}
              </div>
            </div>

            <div style={{ paddingTop: '1rem', borderTop: '1px solid #1e293b' }}>
              <p style={{ fontSize: '0.8125rem', color: '#94a3b8' }}>
                Theme: <strong>Dark Cyber (Default)</strong> • Storage: <strong>Local Workspace Persistence</strong>
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
