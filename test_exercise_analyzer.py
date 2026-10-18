
import unittest

from exercise_analyzer import SquatAnalyzer


class TestSquatAnalyzer(unittest.TestCase):

    def test_complete_squat_counts_one_rep(self):
        analyzer = SquatAnalyzer()

        for angle in [175, 130, 95, 120, 165]:
            reps, _ = analyzer.update(angle)

        self.assertEqual(reps, 1)

    def test_partial_squat_does_not_count(self):
        analyzer = SquatAnalyzer()

        for angle in [175, 130, 120, 165]:
            reps, _ = analyzer.update(angle)

        self.assertEqual(reps, 0)

    def test_missing_angle_preserves_state_and_count(self):
        analyzer = SquatAnalyzer()
        analyzer.update(130)

        old_state = analyzer.state
        old_reps = analyzer.reps

        analyzer.update(None)

        self.assertEqual(analyzer.state, old_state)
        self.assertEqual(analyzer.reps, old_reps)

    def test_invalid_angle_preserves_state_and_count(self):
        analyzer = SquatAnalyzer()
        analyzer.update(130)

        old_state = analyzer.state
        old_reps = analyzer.reps

        analyzer.update(200)

        self.assertEqual(analyzer.state, old_state)
        self.assertEqual(analyzer.reps, old_reps)

    def test_reset_clears_count_and_state(self):
        analyzer = SquatAnalyzer()

        for angle in [175, 130, 95, 165]:
            analyzer.update(angle)

        analyzer.reset()

        self.assertEqual(analyzer.reps, 0)
        self.assertEqual(analyzer.state, "standing")


if __name__ == "__main__":
    unittest.main()

    def test_counts_two_consecutive_squats(self):
        analyzer = SquatAnalyzer()

        angles = [
            175, 130, 95, 165,  # Squat 1
            175, 130, 95, 165,  # Squat 2
        ]

        for angle in angles:
            reps, state = analyzer.update(angle)

        self.assertEqual(reps, 2)
        self.assertEqual(analyzer.state, "standing")
