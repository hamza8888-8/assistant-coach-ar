"""Coordinate exercise analysis and AI coaching feedback."""

from ai.coach import generate_feedback
from analysis.exercise_analyzer import SquatAnalyzer


class CoachingPipeline:
    """Coordinate squat analysis and AI coaching."""

    def __init__(self):
        self.analyzer = SquatAnalyzer()

    def reset(self):
        """Reset the exercise analyzer."""
        self.analyzer.reset()

    def process_landmarks(
        self,
        hip,
        knee,
        ankle,
    ) -> dict:
        """Analyze landmarks and return metrics with coaching feedback."""

        reps, state = self.analyzer.update_from_landmarks(
            hip,
            knee,
            ankle,
        )

        # The analyzer calculates the angle internally, so for now
        # we need to calculate the angle separately for the public metrics.
        from analysis.exercise_analyzer import calculate_angle

        knee_angle = calculate_angle(hip, knee, ankle)

        metrics = {
            "knee_angle": knee_angle,
            "reps": reps,
            "state": state,
        }

        return process_metrics(metrics)


def process_metrics(metrics: dict) -> dict:
    """Return exercise metrics and corresponding coaching feedback."""

    if not isinstance(metrics, dict):
        metrics = {}

    safe_metrics = metrics.copy()
    feedback = generate_feedback(safe_metrics)

    return {
        "metrics": safe_metrics,
        "feedback": feedback,
    }