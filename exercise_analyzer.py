
import numpy as np


def calculate_angle(a, b, c):
    """
    Calculate the angle ABC in degrees.
    Each point is an (x, y) or (x, y, z) coordinate.
    Point b is the joint being measured.
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    c = np.asarray(c, dtype=float)

    ba = a - b
    bc = c - b

    denominator = np.linalg.norm(ba) * np.linalg.norm(bc)

    if denominator < 1e-8:
        return None

    cosine = np.dot(ba, bc) / denominator
    cosine = np.clip(cosine, -1.0, 1.0)

    return float(np.degrees(np.arccos(cosine)))


if __name__ == "__main__":
    hip = (0, 0)
    knee = (1, 0)
    ankle = (1, 1)

    angle = calculate_angle(hip, knee, ankle)
    print(f"Knee angle: {angle:.1f} degrees")



class SquatAnalyzer:
    """A simple state machine for counting squat repetitions."""

    def __init__(self):
        self.reps = 0
        self.state = "standing"

    def update(self, knee_angle):
        if knee_angle is None:
            return self.reps, "Landmark unavailable"

        if self.state == "standing":
            if knee_angle < 140:
                self.state = "descending"
            return self.reps, self.state

        if self.state == "descending":
            if knee_angle < 100:
                self.state = "bottom"
            elif knee_angle > 160:
                self.state = "standing"
            return self.reps, self.state

        if self.state == "bottom":
            if knee_angle > 160:
                self.reps += 1
                self.state = "standing"
                return self.reps, "Rep completed"
            return self.reps, self.state


if __name__ == "__main__":
    analyzer = SquatAnalyzer()

    # Simulated knee angles: standing, descending, bottom, standing
    test_angles = [175, 130, 95, 120, 165, 175]

    for angle in test_angles:
        reps, state = analyzer.update(angle)
        print(f"Angle: {angle} | Reps: {reps} | State: {state}")
