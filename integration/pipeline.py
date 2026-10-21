"""Coordinate exercise metrics and AI coaching feedback."""

import math

from ai.coaching_engine import CoachingEngine


_coaching_engine = CoachingEngine()


def _normalize_metrics(metrics: dict) -> dict:
    """Support both legacy and current exercise metric names."""
    normalized = metrics.copy()

    # Repetition count: current name takes precedence.
    if "repetitions" not in normalized and "reps" in normalized:
        normalized["repetitions"] = normalized["reps"]

    # Movement state: current name takes precedence.
    if "movement_state" not in normalized and "state" in normalized:
        normalized["movement_state"] = normalized["state"]

    # Knee angle: normalize the legacy field into the current schema.
    if "mean_knee" not in normalized and "angles" not in normalized:
        if "knee_angle" in normalized:
            normalized["mean_knee"] = normalized["knee_angle"]

    # Mark an explicitly supplied invalid knee angle as unreliable.
    angle = normalized.get("mean_knee")
    if angle is None and isinstance(normalized.get("angles"), dict):
        angle = normalized["angles"].get("mean_knee")

    if angle is not None:
        valid_angle = (
            isinstance(angle, (int, float))
            and not isinstance(angle, bool)
            and math.isfinite(angle)
            and 0 < angle < 180
        )
        if not valid_angle:
            normalized["valid_measurement"] = False

    return normalized


def process_metrics(metrics: dict) -> dict:
    """Return original metrics and feedback generated from normalized metrics."""
    if not isinstance(metrics, dict):
        metrics = {}

    safe_metrics = metrics.copy()
    normalized = _normalize_metrics(safe_metrics)
    feedback = _coaching_engine.generate_feedback(normalized)

    return {
        "metrics": safe_metrics,
        "feedback": feedback,
    }