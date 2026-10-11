import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Activity,
  Bell,
  HelpCircle,
  Menu,
  Search,
  ShieldCheck,
  TrendingDown,
  TrendingUp,
  Zap,
} from 'lucide-react';
import { api } from '../api/client';
import { MarketIndex } from '../types';

interface Props {
  onOpenSearch: () => void;
  onOpenDisclaimer: () => void;
  onOpenMobileNav?: () => void;
}

export const Navbar: React.FC<Props> = ({ onOpenSearch, onOpenDisclaimer, onOpenMobileNav }) => {
  const [indices, setIndices] = useState<MarketIndex[]>([]);
  const [alertCount, setAlertCount] = useState(0);
  const [dataMode, setDataMode] = useState<string>('demo');
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch quick ticker data, alerts count, and active data mode
    api.getMarketOverview()
      .then((data) => setIndices(data.indices || []))
      .catch(() => {});

    api.getAlerts()
      .then((data) => setAlertCount(data.total || 0))
      .catch(() => {});

    api.getSystemStatus()
      .then((data) => setDataMode(data.data_mode || 'demo'))
      .catch(() => {});
  }, []);

  return (
    <header className="navbar-header">
      {/* Brand & Ticker */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        {/* Mobile Hamburger Button */}
        {onOpenMobileNav && (
          <button
            type="button"
            onClick={onOpenMobileNav}
            className="mobile-menu-btn"
            aria-label="Open navigation"
            title="Open navigation"
          >
            <Menu size={20} />
          </button>
        )}

        <Link
          to="/"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.6rem',
            textDecoration: 'none',
            color: '#f8fafc',
            fontWeight: 800,
            fontSize: '1.125rem',
            letterSpacing: '-0.02em',
          }}
        >
          <div
            style={{
              width: '28px',
              height: '28px',
              borderRadius: '6px',
              backgroundColor: '#10b981',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#0b0f17',
              boxShadow: '0 0 12px rgba(16, 185, 129, 0.4)',
              flexShrink: 0,
            }}
          >
            <Activity size={18} strokeWidth={2.5} />
          </div>
          <span className="navbar-brand-text">
            MarketPulse <span style={{ color: '#10b981' }}>AI</span>
          </span>
        </Link>

        {/* Live Index Ticker Ribbon */}
        <div className="nav-ticker-ribbon">
          {indices.slice(0, 3).map((idx) => {
            const isPos = (idx.change_percent ?? 0) >= 0;
            return (
              <div
                key={idx.symbol}
                onClick={() => navigate(`/markets?symbol=${idx.symbol}`)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.45rem',
                  fontSize: '0.75rem',
                  fontFamily: 'var(--font-mono)',
                  cursor: 'pointer',
                }}
              >
                <span style={{ color: '#94a3b8', fontWeight: 600 }}>{idx.symbol}</span>
                <span style={{ color: '#f8fafc', fontWeight: 700 }}>{idx.value.toLocaleString()}</span>
                <span
                  style={{
                    color: isPos ? '#34d399' : '#f87171',
                    display: 'flex',
                    alignItems: 'center',
                    fontWeight: 600,
                  }}
                >
                  {isPos ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
                  {isPos ? '+' : ''}
                  {idx.change_percent?.toFixed(2)}%
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Global Actions */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
        {/* Search button trigger */}
        <button
          onClick={onOpenSearch}
          className="card-hover"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.6rem',
            background: '#111827',
            border: '1px solid #1e293b',
            padding: '0.4rem 0.85rem',
            borderRadius: '8px',
            color: '#94a3b8',
            fontSize: '0.8125rem',
            cursor: 'pointer',
          }}
        >
          <Search size={15} style={{ color: '#38bdf8' }} />
          <span>Search everything...</span>
          <kbd
            style={{
              fontSize: '0.7rem',
              backgroundColor: '#1e293b',
              padding: '0.15rem 0.35rem',
              borderRadius: '4px',
              color: '#64748b',
              marginLeft: '0.5rem',
              fontFamily: 'var(--font-mono)',
            }}
          >
            /
          </kbd>
        </button>

        {/* Alerts Link */}
        <Link
          to="/alerts"
          className="card-hover"
          style={{
            position: 'relative',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            width: '36px',
            height: '36px',
            borderRadius: '8px',
            background: '#111827',
            border: '1px solid #1e293b',
            color: '#94a3b8',
            textDecoration: 'none',
          }}
          title="Active Intelligence Alerts"
        >
          <Bell size={16} />
          {alertCount > 0 && (
            <span
              style={{
                position: 'absolute',
                top: '-4px',
                right: '-4px',
                width: '18px',
                height: '18px',
                borderRadius: '50%',
                backgroundColor: '#ef4444',
                color: '#fff',
                fontSize: '0.65rem',
                fontWeight: 700,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              {alertCount}
            </span>
          )}
        </Link>

        {/* Data Mode status badge */}
        <Link
          to="/system"
          className={`badge ${dataMode === 'live' ? 'badge-live' : 'badge-demo'}`}
          style={{ textDecoration: 'none', cursor: 'pointer', height: '32px' }}
          title={`Active data mode: ${dataMode.toUpperCase()}`}
        >
          <ShieldCheck size={14} />
          {dataMode === 'live' ? 'LIVE MODE' : 'DEMO MODE'}
        </Link>

        {/* Disclaimer button */}
        <button
          onClick={onOpenDisclaimer}
          style={{
            background: 'none',
            border: 'none',
            color: '#64748b',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            padding: '0.25rem',
          }}
          title="View Educational Disclaimers"
        >
          <HelpCircle size={18} />
        </button>
      </div>
    </header>
  );
};
