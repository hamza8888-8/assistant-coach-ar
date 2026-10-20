def generate_feedback(metrics: dict) -> dict:
    """Generate basic coaching feedback from exercise metrics."""
    if not isinstance(metrics, dict) or not metrics:
        return {
            "message": "Waiting for exercise data.",
            "status": "waiting",
        }

    knee_angle = metrics.get("knee_angle")

    if knee_angle is None:
        return {
            "message": "Knee angle unavailable.",
            "status": "waiting",
        }

    try:
        knee_angle = float(knee_angle)
    except (TypeError, ValueError):
        return {
            "message": "Invalid knee-angle measurement.",
            "status": "waiting",
        }

    if not 0 <= knee_angle <= 180:
        return {
            "message": "Invalid knee-angle measurement.",
            "status": "waiting",
        }

    if knee_angle < 70:
        return {
            "message": "Use a comfortable range of motion and maintain control.",
            "status": "warning",
        }

    return {
        "message": "Keep going! Maintain controlled movement.",
        "status": "good",
    }
