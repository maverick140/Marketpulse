"""Explainable financial sentiment analysis engine.

Uses financial lexicon and token weighting to classify sentiment into positive,
neutral, or negative with normalized score [-1.0, 1.0] and confidence [0.0, 1.0].
"""

from __future__ import annotations

from datetime import datetime, timezone
import re
from typing import Literal

SentimentLabel = Literal["positive", "neutral", "negative"]

POSITIVE_WORDS = {
    "growth", "surge", "gain", "gains", "profit", "profits", "profitable", "beat",
    "beats", "strong", "robust", "rise", "rises", "rising", "high", "higher",
    "record", "bullish", "recovery", "expansion", "upgrade", "outperform",
    "dividend", "boost", "boosts", "rally", "rallies", "optimism", "positive",
    "exceed", "exceeds", "innovative", "accelerate", "breakthrough", "success",
    "advancing", "improved", "improving", "upside", "milestone",
}

NEGATIVE_WORDS = {
    "loss", "losses", "decline", "declines", "declining", "drop", "drops", "dropping",
    "slump", "fall", "falls", "falling", "bearish", "recession", "inflation", "deficit",
    "downgrade", "underperform", "weak", "weakness", "plunge", "plunges", "risk",
    "risks", "crisis", "sanction", "sanctions", "disruption", "disruptions", "investigation",
    "penalty", "fraud", "lawsuit", "default", "pessimism", "negative", "caution",
    "slowdown", "downside", "struggling", "warning", "headwind", "headwinds",
}

INTENSIFIERS = {
    "very": 1.5,
    "substantially": 1.6,
    "significantly": 1.5,
    "strongly": 1.5,
    "sharply": 1.7,
    "massively": 1.8,
    "slightly": 0.6,
    "marginally": 0.5,
}

NEGATORS = {"not", "no", "never", "hardly", "barely", "scarcely", "without"}


def clean_text(text: str) -> list[str]:
    """Clean and tokenize text for sentiment scoring."""
    if not text:
        return []
    cleaned = re.sub(r"[^a-zA-Z\s]", " ", text.lower())
    return [word for word in cleaned.split() if len(word) > 1]


def analyze_text(text: str) -> dict:
    """Analyze financial sentiment for a given text snippet."""
    if not text or not text.strip():
        return {
            "score": 0.0,
            "label": "neutral",
            "confidence": 0.5,
            "positive_count": 0,
            "negative_count": 0,
            "total_tokens": 0,
            "model": "Financial Lexicon v1",
            "version": "1.0.0",
            "timestamp": datetime.now(timezone.utc),
        }

    tokens = clean_text(text)
    if not tokens:
        return {
            "score": 0.0,
            "label": "neutral",
            "confidence": 0.5,
            "positive_count": 0,
            "negative_count": 0,
            "total_tokens": 0,
            "model": "Financial Lexicon v1",
            "version": "1.0.0",
            "timestamp": datetime.now(timezone.utc),
        }

    pos_score = 0.0
    neg_score = 0.0
    pos_count = 0
    neg_count = 0

    for i, token in enumerate(tokens):
        # Look back 1-2 tokens for negators or intensifiers
        intensity = 1.0
        negated = False

        if i > 0 and tokens[i - 1] in INTENSIFIERS:
            intensity = INTENSIFIERS[tokens[i - 1]]
        if i > 0 and tokens[i - 1] in NEGATORS:
            negated = True
        elif i > 1 and tokens[i - 2] in NEGATORS:
            negated = True

        if token in POSITIVE_WORDS:
            if negated:
                neg_score += 1.0 * intensity
                neg_count += 1
            else:
                pos_score += 1.0 * intensity
                pos_count += 1
        elif token in NEGATIVE_WORDS:
            if negated:
                pos_score += 0.8 * intensity
                pos_count += 1
            else:
                neg_score += 1.0 * intensity
                neg_count += 1

    total_sentiment_tokens = pos_count + neg_count
    if total_sentiment_tokens == 0:
        return {
            "score": 0.0,
            "label": "neutral",
            "confidence": 0.6,
            "positive_count": 0,
            "negative_count": 0,
            "total_tokens": len(tokens),
            "model": "Financial Lexicon v1",
            "version": "1.0.0",
            "timestamp": datetime.now(timezone.utc),
        }

    raw_diff = pos_score - neg_score
    max_possible = max(pos_score + neg_score, 1.0)
    score = round(max(min(raw_diff / max_possible, 1.0), -1.0), 2)

    if score > 0.15:
        label: SentimentLabel = "positive"
    elif score < -0.15:
        label = "negative"
    else:
        label = "neutral"

    # Confidence based on density of sentiment tokens
    density = min(total_sentiment_tokens / max(len(tokens), 1), 1.0)
    confidence = round(min(0.5 + (abs(score) * 0.3) + (density * 0.2), 0.95), 2)

    return {
        "score": score,
        "label": label,
        "confidence": confidence,
        "positive_count": pos_count,
        "negative_count": neg_count,
        "total_tokens": len(tokens),
        "model": "Financial Lexicon v1",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc),
    }
