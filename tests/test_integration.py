import unittest

from integration.pipeline import process_metrics


class TestIntegrationPipeline(unittest.TestCase):
    def test_valid_metrics(self):
        result = process_metrics({
            "knee_angle": 90,
            "reps": 3,
            "state": "standing",
        })

        self.assertIn("metrics", result)
        self.assertIn("feedback", result)
        self.assertEqual(result["metrics"]["reps"], 3)
        self.assertEqual(result["feedback"]["status"], "good")

    def test_missing_knee_angle(self):
        result = process_metrics({"reps": 0})

        self.assertEqual(result["feedback"]["status"], "waiting")

    def test_empty_metrics(self):
        result = process_metrics({})

        self.assertEqual(result["metrics"], {})
        self.assertEqual(result["feedback"]["status"], "waiting")

    def test_invalid_input_type(self):
        result = process_metrics(None)

        self.assertEqual(result["metrics"], {})
        self.assertEqual(result["feedback"]["status"], "waiting")

    def test_input_is_not_modified(self):
        metrics = {"knee_angle": 90, "reps": 2}
        original = metrics.copy()

        process_metrics(metrics)

        self.assertEqual(metrics, original)


if __name__ == "__main__":
    unittest.main()
