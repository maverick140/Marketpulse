import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  Clock,
  ExternalLink,
  Filter,
  Newspaper,
  Search,
  Sparkles,
} from 'lucide-react';
import { api } from '../api/client';
import { ProvenanceBadge } from '../components/ProvenanceBadge';
import { NewsArticle } from '../types';

const CATEGORIES = [
  'ALL',
  'MARKET',
  'TECHNOLOGY',
  'COMMODITIES',
  'MACRO',
  'GEOPOLITICS',
  'REGULATORY',
];

function formatTimeAgo(isoString: string, ageHours?: number): string {
  if (ageHours !== undefined && ageHours !== null) {
    if (ageHours < 1) {
      const mins = Math.max(1, Math.round(ageHours * 60));
      return `${mins}m ago`;
    }
    if (ageHours < 24) {
      return `${Math.round(ageHours)}h ago`;
    }
    if (ageHours < 48) {
      return 'Yesterday';
    }
    const days = Math.round(ageHours / 24);
    return `${days}d ago`;
  }
  const diffMs = Math.max(0, Date.now() - new Date(isoString).getTime());
  const diffH = diffMs / (1000 * 60 * 60);
  if (diffH < 1) return `${Math.max(1, Math.round(diffH * 60))}m ago`;
  if (diffH < 24) return `${Math.round(diffH)}h ago`;
  if (diffH < 48) return 'Yesterday';
  return `${Math.round(diffH / 24)}d ago`;
}

export const NewsPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const queryParam = searchParams.get('q') || '';
  const categoryParam = searchParams.get('category') || 'ALL';

  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [total, setTotal] = useState(0);
  const [dataStatus, setDataStatus] = useState<string>('live');
  const [searchQuery, setSearchQuery] = useState(queryParam);
  const [selectedCategory, setSelectedCategory] = useState(categoryParam);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    const cat = selectedCategory === 'ALL' ? '' : selectedCategory;
    api.getNews({ q: searchQuery, category: cat, page: 1, page_size: 40 })
      .then((res) => {
        setArticles(res.articles || []);
        setTotal(res.total || 0);
        if (res.data_status) {
          setDataStatus(res.data_status);
        }
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [searchQuery, selectedCategory]);

  return (
    <div className="content-wrapper animate-fade">
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '1.5rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.25rem' }}>
            <h1 style={{ fontSize: '1.75rem', fontWeight: 800 }}>News Intelligence</h1>
            <ProvenanceBadge status={dataStatus} />
          </div>
          <p style={{ color: '#94a3b8', fontSize: '0.875rem' }}>
            Real-time financial news monitoring with UTC timestamps, strict recency enforcement, and entity attribution.
          </p>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="card" style={{ marginBottom: '1.5rem', padding: '1rem' }}>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'center' }}>
          <div style={{ position: 'relative', flex: 1, minWidth: '260px' }}>
            <Search size={16} style={{ position: 'absolute', left: '12px', top: '13px', color: '#64748b' }} />
            <input
              type="text"
              className="input"
              placeholder="Search latest headlines, ticker symbols, or macro keywords..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{ paddingLeft: '2.25rem' }}
            />
          </div>

          <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
            {CATEGORIES.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                style={{
                  backgroundColor: selectedCategory === cat ? '#10b981' : '#1e293b',
                  color: selectedCategory === cat ? '#0b0f17' : '#cbd5e1',
                  border: 'none',
                  padding: '0.4rem 0.75rem',
                  borderRadius: '6px',
                  fontSize: '0.75rem',
                  fontWeight: 700,
                  cursor: 'pointer',
                  transition: 'all 0.15s',
                }}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Articles Feed */}
      {loading ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {[1, 2, 3].map((i) => (
            <div key={i} className="skeleton" style={{ height: '140px' }} />
          ))}
        </div>
      ) : articles.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '3rem', color: '#64748b' }}>
          <Newspaper size={36} style={{ margin: '0 auto 0.75rem auto', opacity: 0.5 }} />
          <p style={{ fontSize: '1rem', fontWeight: 600, color: '#94a3b8' }}>No recent market news is currently available.</p>
          <p style={{ fontSize: '0.8125rem', marginTop: '0.25rem' }}>Try clearing your search query or selecting a different category filter.</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {articles.map((item, idx) => (
            <div key={item.id || idx} className="card card-hover">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
                  <span className="badge badge-cached">{item.category}</span>
                  {item.freshness === 'CURRENT' && (
                    <span className="badge badge-live" style={{ fontSize: '0.7rem' }}>CURRENT</span>
                  )}
                  {item.freshness === 'RECENT' && (
                    <span className="badge badge-cached" style={{ fontSize: '0.7rem' }}>RECENT</span>
                  )}
                  {item.freshness === 'BACKGROUND' && (
                    <span className="badge badge-demo" style={{ fontSize: '0.7rem' }}>BACKGROUND</span>
                  )}
                  <ProvenanceBadge status={item.data_status} provider={item.provider} />
                  {item.author && <span style={{ fontSize: '0.75rem', color: '#64748b' }}>By {item.author}</span>}
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span style={{ fontSize: '0.75rem', fontWeight: 600, color: '#38bdf8', fontFamily: 'var(--font-mono)' }}>
                    <Clock size={12} style={{ display: 'inline', marginRight: '3px', verticalAlign: 'middle' }} />
                    {formatTimeAgo(item.published_at, item.age_hours)}
                  </span>
                  <span style={{ fontSize: '0.72rem', color: '#64748b', fontFamily: 'var(--font-mono)' }}>
                    ({new Date(item.published_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })})
                  </span>
                </div>
              </div>

              <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: '#f8fafc', marginBottom: '0.4rem' }}>
                {item.headline}
              </h3>

              <p style={{ fontSize: '0.875rem', color: '#cbd5e1', lineHeight: 1.6, marginBottom: '0.85rem' }}>
                {item.summary}
              </p>

              {/* Related entities & sectors */}
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.5rem', paddingTop: '0.6rem', borderTop: '1px solid #1e293b' }}>
                <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
                  {item.related_entities?.map((ent) => (
                    <span
                      key={ent}
                      style={{
                        backgroundColor: '#1e293b',
                        color: '#38bdf8',
                        padding: '0.15rem 0.45rem',
                        borderRadius: '4px',
                        fontSize: '0.72rem',
                        fontWeight: 600,
                        fontFamily: 'var(--font-mono)',
                      }}
                    >
                      #{ent}
                    </span>
                  ))}
                </div>

                <span style={{ fontSize: '0.75rem', color: '#64748b' }}>
                  Source: <strong>{item.source}</strong>
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
