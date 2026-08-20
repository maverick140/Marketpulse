export interface MarketQuote {
  symbol: string;
  name: string;
  price: number;
  change: number | null;
  change_percent: number | null;
  volume: number | null;
  timestamp: string;
  provider: string;
  data_status: string;
  source?: string;
  source_url?: string;
  sector?: string;
  retrieved_at?: string;
}

export interface MarketIndex {
  symbol: string;
  name: string;
  value: number;
  change: number | null;
  change_percent: number | null;
  timestamp: string;
  provider: string;
  data_status: string;
  source?: string;
}

export interface MarketOverview {
  indices: MarketIndex[];
  gainers: MarketQuote[];
  decliners: MarketQuote[];
  most_active: MarketQuote[];
  data_status: string;
  retrieved_at: string;
}

export interface HistoricalPoint {
  timestamp: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface MarketHistory {
  symbol: string;
  timeframe: string;
  data_status: string;
  provider: string;
  points: HistoricalPoint[];
}

export interface TechnicalIndicators {
  symbol: string;
  timeframe: string;
  sma_20: number | null;
  sma_50: number | null;
  ema_20: number | null;
  rsi_14: number | null;
  macd: {
    macd_line: number | null;
    signal_line: number | null;
    histogram: number | null;
  };
  volatility: number | null;
  max_drawdown: number | null;
  period_return: number | null;
  disclaimer: string;
}

export interface MacroIndicator {
  indicator: string;
  value: number;
  unit: string;
  period: string;
  previous_value: number | null;
  change: number | null;
  source: string;
  provider: string;
  data_status: string;
  retrieved_at?: string;
}

export interface MacroDetail {
  indicator: string;
  current: MacroIndicator;
  history: { period: string; value: number; date?: string }[];
  data_status: string;
}

export interface NewsArticle {
  id?: string;
  headline: string;
  summary: string;
  source: string;
  source_url?: string;
  published_at: string;
  category: string;
  related_entities: string[];
  related_sectors: string[];
  countries: string[];
  language: string;
  author?: string;
  freshness?: 'CURRENT' | 'RECENT' | 'BACKGROUND' | 'STALE' | string;
  age_hours?: number;
  provider: string;
  data_status: string;
  content_hash?: string;
}

export interface Announcement {
  id?: string;
  title: string;
  category: string;
  announcement_type: string;
  date: string;
  importance: string;
  source: string;
  source_url?: string;
  related_sectors: string[];
  related_entities: string[];
  provider: string;
  data_status: string;
}

export interface SentimentAnalysis {
  overall_score: number;
  overall_label: string;
  confidence: number;
  distribution: { positive: number; neutral: number; negative: number };
  total_articles: number;
  sectors: { sector: string; average_score: number; label: string; article_count: number }[];
  recent_analyses: {
    id?: string;
    headline: string;
    score: number;
    label: string;
    sector: string;
    source: string;
    published_at: string;
  }[];
  data_status: string;
}

export interface GeopoliticalEvent {
  id?: string;
  title: string;
  description?: string;
  region: string;
  country: string;
  category: string;
  severity: number;
  severity_label: string;
  event_date: string;
  market_relevance: number;
  related_sectors: string[];
  affected_assets: string[];
  freshness?: 'CURRENT' | 'RECENT' | 'BACKGROUND' | 'STALE' | string;
  age_hours?: number;
  provider: string;
  data_status: string;
  source: string;
}

export interface AIEvidenceItem {
  source_type: string;
  reference: string;
  note: string;
}

export interface AIInsight {
  query: string;
  summary: string;
  market_context: string;
  macro_factors: string[];
  news_factors: string[];
  sentiment: string;
  geopolitical_factors: string[];
  risk_factors: string[];
  uncertainties: string[];
  evidence: AIEvidenceItem[];
  model: string;
  generated_at: string;
  disclaimer: string;
}

export interface RiskOverview {
  market_risk_score: number;
  risk_tier: string;
  market_regime: string;
  volatility_index: number;
  top_drivers: string[];
  sector_risks: Record<string, number>;
  generated_at: string;
}

export interface ScenarioResult {
  scenario_type: string;
  magnitude: number;
  estimated_market_impact_percent: number;
  simulated_market_price: number;
  sector_impacts: Record<string, number>;
  summary: string;
  disclaimer: string;
}

export interface Alert {
  id: string;
  alert_type: string;
  severity: string;
  entity: string;
  message: string;
  explanation: string;
  dedup_key: string;
  timestamp: string;
  data_status: string;
}

export interface ProviderStatus {
  type: string;
  provider: string;
  status: string;
  mode: string;
  last_success?: string | null;
  last_error?: string | null;
}

export interface SystemStatus {
  application_status: string;
  environment: string;
  data_mode: string;
  database_status: string;
  api_version: string;
}
