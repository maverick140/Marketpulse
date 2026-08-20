import React, { useEffect, useState } from 'react';
import { Route, Routes, useLocation } from 'react-router-dom';
import { DisclaimerModal } from './components/DisclaimerModal';
import { GlobalSearchModal } from './components/GlobalSearchModal';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { AboutPage } from './pages/AboutPage';
import { AIAnalystPage } from './pages/AIAnalystPage';
import { AlertsPage } from './pages/AlertsPage';
import { AnnouncementsPage } from './pages/AnnouncementsPage';
import { DashboardPage } from './pages/DashboardPage';
import { GeopoliticsPage } from './pages/GeopoliticsPage';
import { LandingPage } from './pages/LandingPage';
import { MacroPage } from './pages/MacroPage';
import { MarketsPage } from './pages/MarketsPage';
import { NewsPage } from './pages/NewsPage';
import { RiskLabPage } from './pages/RiskLabPage';
import { SentimentPage } from './pages/SentimentPage';
import { SystemPage } from './pages/SystemPage';
import { WorkspacePage } from './pages/WorkspacePage';

export const App: React.FC = () => {
  const [searchOpen, setSearchOpen] = useState(false);
  const [disclaimerOpen, setDisclaimerOpen] = useState(false);
  const [mobileNavOpen, setMobileNavOpen] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState<boolean>(() => {
    try {
      return localStorage.getItem('marketpulse_sidebar_collapsed') === 'true';
    } catch {
      return false;
    }
  });
  const location = useLocation();

  // Close mobile drawer on route change
  useEffect(() => {
    setMobileNavOpen(false);
  }, [location.pathname]);

  const toggleSidebarCollapse = () => {
    setSidebarCollapsed((prev) => {
      const next = !prev;
      try {
        localStorage.setItem('marketpulse_sidebar_collapsed', String(next));
      } catch (err) {
        console.warn('Unable to persist sidebar state in localStorage', err);
      }
      return next;
    });
  };

  // Keyboard shortcut listener for '/' and 'Ctrl+K'
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (
        (e.key === '/' && !(e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement)) ||
        ((e.metaKey || e.ctrlKey) && e.key === 'k')
      ) {
        e.preventDefault();
        setSearchOpen(true);
      } else if (e.key === 'Escape') {
        setSearchOpen(false);
        setMobileNavOpen(false);
        if (localStorage.getItem('marketpulse_disclaimer_acknowledged') === 'true') {
          setDisclaimerOpen(false);
        }
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const isLanding = location.pathname === '/';

  return (
    <div className="app-container">
      {/* Sidebar (shown on all pages, collapsible on desktop, drawer on mobile) */}
      <Sidebar
        collapsed={sidebarCollapsed}
        onToggleCollapse={toggleSidebarCollapse}
        mobileOpen={mobileNavOpen}
        onCloseMobile={() => setMobileNavOpen(false)}
      />

      {/* Main Content Area */}
      <div className="main-content">
        <Navbar
          onOpenSearch={() => setSearchOpen(true)}
          onOpenDisclaimer={() => setDisclaimerOpen(true)}
          onOpenMobileNav={() => setMobileNavOpen(true)}
        />

        <main style={{ flex: 1 }}>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/markets" element={<MarketsPage />} />
            <Route path="/macro" element={<MacroPage />} />
            <Route path="/news" element={<NewsPage />} />
            <Route path="/sentiment" element={<SentimentPage />} />
            <Route path="/geopolitics" element={<GeopoliticsPage />} />
            <Route path="/ai-analyst" element={<AIAnalystPage />} />
            <Route path="/risk-lab" element={<RiskLabPage />} />
            <Route path="/announcements" element={<AnnouncementsPage />} />
            <Route path="/alerts" element={<AlertsPage />} />
            <Route path="/workspace" element={<WorkspacePage />} />
            <Route path="/system" element={<SystemPage />} />
            <Route path="/dashboard/system" element={<SystemPage />} />
            <Route path="/about" element={<AboutPage onOpenDisclaimer={() => setDisclaimerOpen(true)} />} />
            <Route path="*" element={<DashboardPage />} />
          </Routes>
        </main>
      </div>

      {/* Global Modals */}
      <GlobalSearchModal isOpen={searchOpen} onClose={() => setSearchOpen(false)} />
      <DisclaimerModal forceOpen={disclaimerOpen} onClose={() => setDisclaimerOpen(false)} />
    </div>
  );
};
export default App;
