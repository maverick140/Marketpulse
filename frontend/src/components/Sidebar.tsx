import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  Activity,
  AlertCircle,
  Bell,
  Bookmark,
  Building2,
  ChevronLeft,
  ChevronRight,
  Cpu,
  FileText,
  Flame,
  Globe,
  Info,
  Layers,
  LineChart,
  Newspaper,
  PanelLeftClose,
  PanelLeftOpen,
  Shield,
  X,
  Zap,
} from 'lucide-react';

export const NAV_ITEMS = [
  { path: '/dashboard', label: 'Dashboard', icon: Activity },
  { path: '/markets', label: 'Markets', icon: LineChart },
  { path: '/macro', label: 'Macro Data', icon: Building2 },
  { path: '/news', label: 'News Feed', icon: Newspaper },
  { path: '/sentiment', label: 'Sentiment', icon: Flame },
  { path: '/geopolitics', label: 'Geopolitics', icon: Globe },
  { path: '/ai-analyst', label: 'AI Analyst', icon: Cpu },
  { path: '/risk-lab', label: 'Risk Lab', icon: Shield },
  { path: '/announcements', label: 'Announcements', icon: FileText },
  { path: '/alerts', label: 'Alerts', icon: Bell },
  { path: '/workspace', label: 'Workspace', icon: Bookmark },
  { path: '/system', label: 'System Health', icon: Zap },
  { path: '/about', label: 'About & Scope', icon: Info },
];

interface Props {
  collapsed?: boolean;
  onToggleCollapse?: () => void;
  mobileOpen?: boolean;
  onCloseMobile?: () => void;
}

export const Sidebar: React.FC<Props> = ({
  collapsed = false,
  onToggleCollapse,
  mobileOpen = false,
  onCloseMobile,
}) => {
  const handleNavClick = () => {
    if (mobileOpen && onCloseMobile) {
      onCloseMobile();
    }
  };

  return (
    <>
      {/* Mobile Backdrop Overlay */}
      {mobileOpen && (
        <div
          className="sidebar-backdrop"
          onClick={onCloseMobile}
          role="presentation"
          aria-label="Close navigation"
        />
      )}

      <aside
        className={`sidebar-container ${collapsed ? 'collapsed' : ''} ${mobileOpen ? 'mobile-open' : ''}`}
        aria-label="Primary Navigation"
      >
        {/* Sidebar Header & Collapse/Close Controls */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: collapsed ? 'center' : 'space-between',
            padding: collapsed ? '1rem 0.5rem 0.5rem' : '1rem 0.75rem 0.5rem',
            borderBottom: '1px solid #162032',
            minHeight: '52px',
          }}
        >
          {!collapsed && (
            <span
              style={{
                fontSize: '0.65rem',
                fontWeight: 700,
                textTransform: 'uppercase',
                color: '#64748b',
                letterSpacing: '0.08em',
                paddingLeft: '0.25rem',
              }}
            >
              Intelligence Hub
            </span>
          )}

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
            {/* Desktop Collapse/Expand Button */}
            {onToggleCollapse && (
              <button
                type="button"
                onClick={onToggleCollapse}
                className="btn-sidebar-toggle desktop-toggle"
                aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
                title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
              >
                {collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
              </button>
            )}

            {/* Mobile Close Button */}
            {onCloseMobile && (
              <button
                type="button"
                onClick={onCloseMobile}
                className="btn-sidebar-toggle mobile-close-btn"
                aria-label="Close navigation"
                title="Close navigation"
              >
                <X size={18} />
              </button>
            )}
          </div>
        </div>

        {/* Navigation List */}
        <div style={{ padding: collapsed ? '0.75rem 0.35rem' : '0.75rem 0.65rem', flex: 1, overflowY: 'auto' }}>
          <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
            {NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  onClick={handleNavClick}
                  className={({ isActive }) =>
                    `sidebar-link ${isActive ? 'active' : ''}`
                  }
                  title={collapsed ? item.label : undefined}
                >
                  <Icon size={18} style={{ flexShrink: 0 }} />
                  {!collapsed && <span className="sidebar-link-label">{item.label}</span>}
                  {collapsed && <span className="sidebar-tooltip">{item.label}</span>}
                </NavLink>
              );
            })}
          </nav>
        </div>

        {/* Footer Info Badge */}
        <div
          style={{
            padding: collapsed ? '0.75rem 0.35rem' : '0.85rem 0.75rem',
            borderTop: '1px solid #1e293b',
            backgroundColor: '#0b0f17',
            display: 'flex',
            flexDirection: 'column',
            gap: '0.25rem',
            alignItems: collapsed ? 'center' : 'stretch',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: collapsed ? 'center' : 'space-between', width: '100%' }}>
            {!collapsed && <span style={{ fontSize: '0.72rem', color: '#64748b', fontWeight: 600 }}>v1.0.0 Portfolio</span>}
            <span
              style={{
                width: '8px',
                height: '8px',
                borderRadius: '50%',
                backgroundColor: '#10b981',
                boxShadow: '0 0 6px rgba(16, 185, 129, 0.6)',
              }}
              title="System Online (v1.0.0)"
            />
          </div>
          {!collapsed && (
            <p style={{ fontSize: '0.68rem', color: '#475569', lineHeight: 1.3 }}>
              Educational Platform • No Advice
            </p>
          )}
        </div>
      </aside>
    </>
  );
};
