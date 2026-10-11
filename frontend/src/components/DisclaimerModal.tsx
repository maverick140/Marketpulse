import React, { useEffect, useState } from 'react';
import { AlertTriangle, BookOpen, CheckCircle2, Info, ShieldAlert } from 'lucide-react';

interface Props {
  forceOpen?: boolean;
  onClose?: () => void;
}

export const STORAGE_KEY = 'marketpulse_disclaimer_acknowledged';

export const DisclaimerModal: React.FC<Props> = ({ forceOpen, onClose }) => {
  const [isOpen, setIsOpen] = useState<boolean>(() => {
    try {
      const acknowledged = localStorage.getItem(STORAGE_KEY) || localStorage.getItem('marketpulse_disclaimer_ack');
      return !acknowledged;
    } catch {
      return true;
    }
  });

  useEffect(() => {
    if (forceOpen === true) {
      setIsOpen(true);
    } else if (forceOpen === false && (localStorage.getItem(STORAGE_KEY) || localStorage.getItem('marketpulse_disclaimer_ack'))) {
      setIsOpen(false);
    }
  }, [forceOpen]);

  const handleAccept = () => {
    try {
      localStorage.setItem(STORAGE_KEY, 'true');
      localStorage.setItem('marketpulse_disclaimer_ack', 'true');
    } catch (err) {
      console.warn('Unable to persist disclaimer acceptance in localStorage', err);
    }
    setIsOpen(false);
    if (onClose) onClose();
  };

  if (!isOpen) return null;

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(3, 7, 18, 0.88)',
        backdropFilter: 'blur(10px)',
        WebkitBackdropFilter: 'blur(10px)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 99999,
        padding: '1.25rem',
        overflowY: 'auto',
      }}
      role="dialog"
      aria-modal="true"
      aria-labelledby="disclaimer-title"
      aria-describedby="disclaimer-desc"
    >
      <div
        className="card animate-fade"
        style={{
          maxWidth: '560px',
          width: '100%',
          backgroundColor: '#0f172a',
          borderColor: '#1e293b',
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.85), 0 0 0 1px rgba(255, 255, 255, 0.05)',
          padding: '1.75rem',
          borderRadius: '12px',
          margin: 'auto',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.25rem' }}>
          <div
            style={{
              width: '40px',
              height: '40px',
              borderRadius: '10px',
              backgroundColor: 'rgba(245, 158, 11, 0.15)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#fbbf24',
              flexShrink: 0,
              border: '1px solid rgba(245, 158, 11, 0.25)',
            }}
          >
            <ShieldAlert size={22} />
          </div>
          <div>
            <h2 id="disclaimer-title" style={{ fontSize: '1.25rem', fontWeight: 800, color: '#f8fafc', lineHeight: 1.2 }}>
              Important Notice
            </h2>
            <p style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '0.2rem' }}>
              MarketPulse AI Educational & Research Platform
            </p>
          </div>
        </div>

        {/* Body */}
        <div id="disclaimer-desc" style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', color: '#cbd5e1', fontSize: '0.875rem', lineHeight: 1.6 }}>
          <p>
            MarketPulse AI is an educational and research platform designed to help users explore market data, news, macroeconomic indicators, geopolitical developments, and AI-assisted analysis.
          </p>

          <p>
            Market data and news may be delayed, incomplete, inaccurate, or subject to provider limitations.
          </p>

          <p>
            AI-generated analysis is informational only and may contain errors. It is not financial advice, investment advice, trading advice, or a recommendation to buy or sell any security.
          </p>

          <p style={{ color: '#94a3b8', fontSize: '0.8125rem' }}>
            Always verify important information using reliable primary sources before making financial decisions.
          </p>
        </div>

        {/* Action Button with Left-to-Right Animated Fill */}
        <div
          style={{
            marginTop: '1.5rem',
            paddingTop: '1.25rem',
            borderTop: '1px solid #1e293b',
          }}
        >
          <button
            type="button"
            onClick={handleAccept}
            className="btn-disclaimer-understand"
            aria-label="I Understand"
            autoFocus
          >
            I Understand
          </button>
        </div>
      </div>
    </div>
  );
};
