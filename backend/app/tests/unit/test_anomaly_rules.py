from app.domain.services.anomaly_service import anomaly_score, classify_level


def test_anomaly_score_in_range():
    assert anomaly_score(30, 20, 50) == 0


def test_anomaly_score_out_of_range_and_level():
    score = anomaly_score(80, 20, 50)
    assert score > 0
    assert classify_level(score).value in {"critica", "alta", "media", "baja"}
