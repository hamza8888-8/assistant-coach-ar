"""Coordinate exercise metrics and AI coaching feedback."""

from ai.coach import generate_feedback


def process_metrics(metrics: dict) -> dict:
    """Return exercise metrics and corresponding coaching feedback."""
    if not isinstance(metrics, dict):
        metrics = {}

    # Copy the input so this function does not modify the caller's dictionary.
    safe_metrics = metrics.copy()
    feedback = generate_feedback(safe_metrics)

    return {
        "metrics": safe_metrics,
        "feedback": feedback,
    }
