
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
