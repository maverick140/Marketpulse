import React from 'react';
import { TrendingDown, TrendingUp } from 'lucide-react';

interface Props {
  title: string;
  value: string | number;
  change?: number | null;
  changePercent?: number | null;
  subtitle?: string;
  badge?: React.ReactNode;
  icon?: React.ReactNode;
  variant?: 'default' | 'emerald' | 'ruby' | 'cyan';
  onClick?: () => void;
}

export const MetricCard: React.FC<Props> = ({
  title,
  value,
  change,
  changePercent,
  subtitle,
  badge,
  icon,
  variant = 'default',
  onClick,
}) => {
  const isPositive = (changePercent ?? change ?? 0) >= 0;
  const isNeutral = changePercent === null && change === null;

  return (
    <div
      onClick={onClick}
      className={`card ${onClick ? 'card-hover cursor-pointer' : ''} ${
        variant === 'emerald'
          ? 'card-glow-emerald'
          : variant === 'ruby'
          ? 'card-glow-ruby'
          : variant === 'cyan'
          ? 'card-glow-cyan'
          : ''
      }`}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
        <span style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', fontWeight: 500 }}>
          {title}
        </span>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          {badge}
          {icon && <span style={{ color: 'var(--text-muted)' }}>{icon}</span>}
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.75rem', marginTop: '0.25rem' }}>
        <span style={{ fontSize: '1.5rem', fontWeight: 700, fontFamily: 'var(--font-mono)' }}>
          {value}
        </span>

        {!isNeutral && (
          <span
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.2rem',
              fontSize: '0.8125rem',
              fontWeight: 600,
              fontFamily: 'var(--font-mono)',
              color: isPositive ? 'var(--color-emerald)' : 'var(--color-ruby)',
            }}
          >
            {isPositive ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
            {changePercent !== undefined && changePercent !== null
              ? `${changePercent >= 0 ? '+' : ''}${changePercent.toFixed(2)}%`
              : `${change !== undefined && change !== null ? (change >= 0 ? '+' : '') + change.toFixed(2) : ''}`}
          </span>
        )}
      </div>

      {subtitle && (
        <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.4rem' }}>
          {subtitle}
        </p>
      )}
    </div>
  );
};
