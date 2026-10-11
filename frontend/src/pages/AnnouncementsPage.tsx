import React, { useEffect, useState } from 'react';
import { Calendar, FileText, Tag } from 'lucide-react';
import { api } from '../api/client';
import { ProvenanceBadge } from '../components/ProvenanceBadge';
import { Announcement } from '../types';

export const AnnouncementsPage: React.FC = () => {
  const [announcements, setAnnouncements] = useState<Announcement[]>([]);
  const [category, setCategory] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api.getAnnouncements(category)
      .then((res) => setAnnouncements(res.announcements || []))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [category]);

  const CATEGORIES = ['', 'COMPANY', 'ECONOMY', 'REGULATORY', 'POLICY'];

  return (
    <div className="content-wrapper animate-fade">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '1.5rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.25rem' }}>
            <h1 style={{ fontSize: '1.75rem', fontWeight: 800 }}>Corporate & Regulatory Announcements</h1>
            <ProvenanceBadge status="demo" />
          </div>
          <p style={{ color: '#94a3b8', fontSize: '0.875rem' }}>
            Official corporate releases, central-bank calendar notices, and capital market regulatory updates.
          </p>
        </div>
      </div>

      {/* Category filter tabs */}
      <div style={{ display: 'flex', gap: '0.4rem', marginBottom: '1.5rem' }}>
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            onClick={() => setCategory(cat)}
            style={{
              backgroundColor: category === cat ? '#10b981' : '#1e293b',
              color: category === cat ? '#0b0f17' : '#cbd5e1',
              border: 'none',
              padding: '0.4rem 0.75rem',
              borderRadius: '6px',
              fontSize: '0.75rem',
              fontWeight: 700,
              cursor: 'pointer',
            }}
          >
            {cat || 'ALL CATEGORIES'}
          </button>
        ))}
      </div>

      {/* Announcements Feed */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
        {announcements.map((ann) => (
          <div key={ann.id} className="card card-hover">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.35rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span className={`badge ${ann.importance === 'high' ? 'badge-critical' : ann.importance === 'medium' ? 'badge-warning' : 'badge-info'}`}>
                  {ann.importance.toUpperCase()} PRIORITY
                </span>
                <span className="badge badge-cached">{ann.category}</span>
                <span style={{ fontSize: '0.75rem', color: '#64748b' }}>{ann.announcement_type}</span>
              </div>
              <span style={{ fontSize: '0.75rem', color: '#64748b', fontFamily: 'var(--font-mono)' }}>
                {ann.date}
              </span>
            </div>

            <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#f8fafc', marginBottom: '0.4rem' }}>
              {ann.title}
            </h3>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '0.5rem', borderTop: '1px solid #1e293b' }}>
              <div style={{ display: 'flex', gap: '0.4rem' }}>
                {ann.related_entities?.map((ent) => (
                  <span key={ent} style={{ backgroundColor: '#1e293b', color: '#38bdf8', padding: '0.1rem 0.4rem', borderRadius: '4px', fontSize: '0.72rem', fontWeight: 600 }}>
                    #{ent}
                  </span>
                ))}
              </div>
              <span style={{ fontSize: '0.72rem', color: '#64748b' }}>Source: {ann.source}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
