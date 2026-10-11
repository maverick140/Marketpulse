import React from 'react';
import { AlertTriangle, Database, FileCheck, ShieldCheck, Zap } from 'lucide-react';

interface Props {
  status: string;
  provider?: string;
  className?: string;
}

export const ProvenanceBadge: React.FC<Props> = ({ status, provider, className = '' }) => {
  const normalized = (status || 'demo').toLowerCase();

  if (normalized === 'live') {
    return (
      <span className={`badge badge-live ${className}`}>
        <Zap className="w-3 h-3 text-emerald-400" />
        LIVE {provider ? `• ${provider.toUpperCase()}` : ''}
      </span>
    );
  }

  if (normalized === 'official') {
    return (
      <span className={`badge badge-cached ${className}`}>
        <FileCheck className="w-3 h-3 text-cyan-400" />
        OFFICIAL {provider ? `• ${provider.toUpperCase()}` : ''}
      </span>
    );
  }

  if (normalized === 'cached') {
    return (
      <span className={`badge badge-cached ${className}`}>
        <Database className="w-3 h-3 text-blue-400" />
        CACHED {provider ? `• ${provider.toUpperCase()}` : ''}
      </span>
    );
  }

  if (normalized === 'unavailable') {
    return (
      <span className={`badge badge-warning ${className}`} style={{ borderColor: 'rgba(244, 63, 94, 0.4)', color: '#fb7185' }}>
        <AlertTriangle className="w-3 h-3 text-rose-400" />
        UNAVAILABLE {provider ? `• ${provider.toUpperCase()}` : ''}
      </span>
    );
  }

  return (
    <span className={`badge badge-demo ${className}`}>
      <ShieldCheck className="w-3 h-3 text-amber-400" />
      DEMO DATA
    </span>
  );
};
