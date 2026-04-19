from app.domain.value_objects.enums import AlertLevel


def anomaly_score(value: float, min_threshold: float, max_threshold: float) -> float:
    if min_threshold <= value <= max_threshold:
        return 0.0
    if value < min_threshold:
        distance = min_threshold - value
        baseline = max(min_threshold, 1)
    else:
        distance = value - max_threshold
        baseline = max(max_threshold, 1)
    return round(distance / baseline, 4)


def classify_level(score: float) -> AlertLevel:
    if score >= 0.5:
        return AlertLevel.critica
    if score >= 0.3:
        return AlertLevel.alta
    if score >= 0.15:
        return AlertLevel.media
    return AlertLevel.baja
