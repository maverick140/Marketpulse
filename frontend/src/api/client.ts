import {
  AIInsight,
  Alert,
  Announcement,
  GeopoliticalEvent,
  MacroDetail,
  MacroIndicator,
  MarketHistory,
  MarketOverview,
  MarketQuote,
  NewsArticle,
  RiskOverview,
  ScenarioResult,
  SentimentAnalysis,
  SystemStatus,
  TechnicalIndicators,
} from '../types';

const API_BASE = (((import.meta as any).env?.VITE_API_URL as string) || '').trim();
const BASE_URL = API_BASE ? `${API_BASE.replace(/\/+$/, '')}/api` : '/api';

async function fetchJSON<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const errBody = await response.json().catch(() => ({}));
    const message = errBody?.error?.message || `HTTP ${response.status}: ${response.statusText}`;
    throw new Error(message);
  }

  return response.json();
}

export const api = {
  // Markets
  getMarketOverview: () => fetchJSON<MarketOverview>('/markets/overview'),
  searchMarkets: (q: string) => fetchJSON<{ query: string; results: any[]; count: number }>(`/markets/search?q=${encodeURIComponent(q)}`),
  getQuote: (symbol: string) => fetchJSON<MarketQuote>(`/markets/quote/${encodeURIComponent(symbol)}`),
  getHistory: (symbol: string, tf: string = '1M') => fetchJSON<MarketHistory>(`/markets/history/${encodeURIComponent(symbol)}?timeframe=${encodeURIComponent(tf)}`),
  getIndicators: (symbol: string, tf: string = '1M') => fetchJSON<TechnicalIndicators>(`/markets/indicators/${encodeURIComponent(symbol)}?timeframe=${encodeURIComponent(tf)}`),

  // Macro
  getMacroList: () => fetchJSON<{ indicators: MacroIndicator[]; count: number }>('/macro'),
  getMacroDetail: (name: string) => fetchJSON<MacroDetail>(`/macro/${encodeURIComponent(name)}`),

  // News & Announcements
  getNews: (params: { q?: string; category?: string; symbol?: string; country?: string; freshness?: string; max_age_hours?: number; page?: number; page_size?: number } = {}) => {
    const query = new URLSearchParams();
    if (params.q) query.set('q', params.q);
    if (params.category) query.set('category', params.category);
    if (params.symbol) query.set('symbol', params.symbol);
    if (params.country) query.set('country', params.country);
    if (params.freshness) query.set('freshness', params.freshness);
    if (params.max_age_hours !== undefined) query.set('max_age_hours', params.max_age_hours.toString());
    if (params.page) query.set('page', params.page.toString());
    if (params.page_size) query.set('page_size', params.page_size.toString());
    return fetchJSON<{ articles: NewsArticle[]; total: number; data_status?: string; retrieved_at?: string }>(`/news?${query.toString()}`);
  },
  getSingleNews: (id: string) => fetchJSON<NewsArticle>(`/news/${encodeURIComponent(id)}`),
  getAnnouncements: (category: string = '', importance: string = '') => {
    const query = new URLSearchParams();
    if (category) query.set('category', category);
    if (importance) query.set('importance', importance);
    return fetchJSON<{ announcements: Announcement[]; total: number; data_status?: string }>(`/announcements?${query.toString()}`);
  },

  // Sentiment
  getMarketSentiment: () => fetchJSON<SentimentAnalysis>('/sentiment'),
  getSymbolSentiment: (symbol: string) => fetchJSON<any>(`/sentiment/symbol/${encodeURIComponent(symbol)}`),
  getSentimentTrends: (timeframe: string = '7D') => fetchJSON<{ trends: any[]; timeframe: string }>(`/sentiment/trends?timeframe=${encodeURIComponent(timeframe)}`),
  analyzeText: (text: string) => fetchJSON<any>('/sentiment/analyze', { method: 'POST', body: JSON.stringify({ text }) }),

  // Geopolitics
  getGeopolitics: (params: { country?: string; region?: string; severity?: string; sector?: string } = {}) => {
    const query = new URLSearchParams();
    if (params.country) query.set('country', params.country);
    if (params.region) query.set('region', params.region);
    if (params.severity) query.set('severity', params.severity);
    if (params.sector) query.set('sector', params.sector);
    return fetchJSON<{ events: GeopoliticalEvent[]; total: number; data_status?: string; retrieved_at?: string }>(`/geopolitics?${query.toString()}`);
  },
  getRegions: () => fetchJSON<{ regions: any[]; total_regions: number }>('/geopolitics/regions'),

  // AI Intelligence
  getAIInsights: () => fetchJSON<{ insights: AIInsight[]; total: number }>('/ai/insights'),
  runAIResearch: (payload: { query: string; symbol?: string; sector?: string }) => fetchJSON<AIInsight>('/ai/research', { method: 'POST', body: JSON.stringify(payload) }),

  // Risk & Scenario Lab
  getRiskOverview: () => fetchJSON<RiskOverview>('/risk/overview'),
  getSecurityRisk: (symbol: string) => fetchJSON<any>(`/risk/symbol/${encodeURIComponent(symbol)}`),
  simulateScenario: (scenario_type: string, magnitude: number) => fetchJSON<ScenarioResult>('/risk/scenario', { method: 'POST', body: JSON.stringify({ scenario_type, magnitude }) }),
  getCorrelation: () => fetchJSON<{ assets: string[]; matrix: number[][] }>('/risk/correlation'),

  // Alerts
  getAlerts: (severity: string = '', type: string = '') => {
    const query = new URLSearchParams();
    if (severity) query.set('severity', severity);
    if (type) query.set('type', type);
    return fetchJSON<{ alerts: Alert[]; total: number; critical_count: number; warning_count: number; info_count: number }>(`/alerts?${query.toString()}`);
  },

  // Unified Search
  unifiedSearch: (q: string) => fetchJSON<any>(`/search?q=${encodeURIComponent(q)}`),

  // User Features
  getWatchlist: () => fetchJSON<{ items: any[]; total: number }>('/user/watchlist'),
  addToWatchlist: (symbol: string) => fetchJSON<any>('/user/watchlist', { method: 'POST', body: JSON.stringify({ symbol }) }),
  removeFromWatchlist: (symbol: string) => fetchJSON<any>(`/user/watchlist/${encodeURIComponent(symbol)}`, { method: 'DELETE' }),
  getSavedResearch: () => fetchJSON<{ items: any[]; total: number }>('/user/research'),
  saveResearch: (payload: { title: string; query: string; summary: string; tags: string[] }) => fetchJSON<any>('/user/research', { method: 'POST', body: JSON.stringify(payload) }),
  deleteSavedResearch: (id: string) => fetchJSON<any>(`/user/research/${encodeURIComponent(id)}`, { method: 'DELETE' }),
  getPreferences: () => fetchJSON<any>('/user/preferences'),
  updatePreferences: (payload: any) => fetchJSON<any>('/user/preferences', { method: 'PUT', body: JSON.stringify(payload) }),

  // System & Health
  getHealth: () => fetchJSON<{ status: string }>('/health'),
  getSystemStatus: () => fetchJSON<SystemStatus>('/system/status'),
  getProviders: () => fetchJSON<{ providers: any[] }>('/system/providers'),
};
