"""Unit tests for sentiment analysis engine."""

from app.ml.sentiment import analyze_text, clean_text


def test_clean_text() -> None:
    text = "Infosys Q4 Profit Surges 12% in USD terms!!!"
    tokens = clean_text(text)
    assert "infosys" in tokens
    assert "profit" in tokens
    assert "surges" in tokens
    assert len(tokens) >= 4


def test_positive_sentiment() -> None:
    text = "Company reports record profit growth and strong revenue surge."
    res = analyze_text(text)
    assert res["label"] == "positive"
    assert res["score"] > 0.3
    assert res["confidence"] >= 0.5


def test_negative_sentiment() -> None:
    text = "Severe losses reported amid sharp economic decline and rising inflation risks."
    res = analyze_text(text)
    assert res["label"] == "negative"
    assert res["score"] < -0.3
    assert res["confidence"] >= 0.5


def test_negated_sentiment() -> None:
    text = "The firm did not make any profit and had no growth."
    res = analyze_text(text)
    assert res["label"] in {"negative", "neutral"}
    assert res["score"] <= 0.0


def test_empty_or_neutral_text() -> None:
    empty_res = analyze_text("")
    assert empty_res["label"] == "neutral"
    assert empty_res["score"] == 0.0

    neutral_res = analyze_text("The committee will meet on Thursday afternoon.")
    assert neutral_res["label"] == "neutral"
    assert abs(neutral_res["score"]) <= 0.15
