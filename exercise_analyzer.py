
import numpy as np


def calculate_angle(a, b, c):
    """
    Calculate angle ABC in degrees.
    Each point is an (x, y) or (x, y, z) coordinate.
    Point b is the joint being measured.
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    c = np.asarray(c, dtype=float)

    ba = a - b
    bc = c - b

    denominator = np.linalg.norm(ba) * np.linalg.norm(bc)

    # Avoid division by zero if points overlap.
    if denominator < 1e-8:
        return None

    cosine = np.dot(ba, bc) / denominator
    cosine = np.clip(cosine, -1.0, 1.0)

    return float(np.degrees(np.arccos(cosine)))


class SquatAnalyzer:
    """Analyze knee angles and count completed squat repetitions."""

    def __init__(self):
        self.reps = 0
        self.state = "standing"

    def reset(self):
        """Reset the repetition count and movement state."""
        self.reps = 0
        self.state = "standing"

    def update(self, knee_angle):
        """
        Process one knee-angle measurement.

        Returns:
            (reps, state_or_message)
        """
        # Handle missing measurements.
        if knee_angle is None:
            return self.reps, "Landmark unavailable"

        # Reject angles outside the valid range.
        if not 0 <= knee_angle <= 180:
            return self.reps, "Invalid knee angle"

        # Standing -> descending.
        if self.state == "standing":
            if knee_angle < 140:
                self.state = "descending"

            return self.reps, self.state

        # Descending -> bottom, or return to standing.
        elif self.state == "descending":
            if knee_angle < 100:
                self.state = "bottom"
            elif knee_angle > 160:
                self.state = "standing"

            return self.reps, self.state

        # Bottom -> standing completes a repetition.
        elif self.state == "bottom":
            if knee_angle > 160:
                self.reps += 1
                self.state = "standing"
                return self.reps, "Rep completed"

            return self.reps, self.state

        # Defensive fallback if the state is ever corrupted.
        self.state = "standing"
        return self.reps, "standing"

    def update_from_landmarks(self, hip, knee, ankle):
        """
        Calculate the knee angle from hip, knee, and ankle coordinates,
        then update the squat analyzer.
        """
        if hip is None or knee is None or ankle is None:
            return self.reps, "Landmark unavailable"

        try:
            knee_angle = calculate_angle(hip, knee, ankle)
        except (TypeError, ValueError):
            return self.reps, "Invalid landmark coordinates"

        if knee_angle is None:
            return self.reps, "Landmark unavailable"

        return self.update(knee_angle)


if __name__ == "__main__":
    # Standalone demonstration using simulated angles.
    analyzer = SquatAnalyzer()

    test_angles = [175, 130, 95, 120, 165, 175]

    for angle in test_angles:
        reps, state = analyzer.update(angle)
        print(f"Angle: {angle} | Reps: {reps} | State: {state}")

    print("\nTesting landmark-based analysis:")

    analyzer.reset()

    # These points form a 90-degree angle at the knee.
    hip = (0, 1)
    knee = (0, 0)
    ankle = (1, 0)

    reps, state = analyzer.update_from_landmarks(hip, knee, ankle)

    print(f"Reps: {reps} | State: {state}")
