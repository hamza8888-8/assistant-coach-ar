import unittest

from ai.coach import generate_feedback


class TestGenerateFeedback(unittest.TestCase):
    def test_empty_metrics(self):
        self.assertEqual(generate_feedback({})["status"], "waiting")

    def test_missing_angle(self):
        self.assertEqual(generate_feedback({"reps": 2})["status"], "waiting")

    def test_controlled_movement(self):
        result = generate_feedback({"knee_angle": 90})
        self.assertEqual(result["status"], "good")

    def test_low_angle_warning(self):
        result = generate_feedback({"knee_angle": 60})
        self.assertEqual(result["status"], "warning")

    def test_invalid_angle(self):
        self.assertEqual(
            generate_feedback({"knee_angle": 200})["status"],
            "waiting",
        )


if __name__ == "__main__":
    unittest.main()
