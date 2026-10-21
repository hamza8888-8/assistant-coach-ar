
"""Live AR Sports Coach demo using real MediaPipe pose detection.

Press Q in the video window to quit.
"""

import cv2

from vision.webcam import WebcamCamera
from vision.pose_detector import PoseDetector
from integration.pipeline import CoachingPipeline
from ar.overlay import draw_pipeline_overlay


def main():
    pipeline = CoachingPipeline()

    try:
        with PoseDetector() as detector, WebcamCamera() as camera:
            print("AR Sports Coach started.")
            print("Stand far enough from the camera to show your body.")
            print("Press Q in the video window to quit.")

            while True:
                success, frame = camera.read()

                if not success:
                    print("Could not capture a webcam frame.")
                    break

                detection = detector.detect(frame)
                landmarks = {}
                result = {
                    "metrics": {
                        "knee_angle": None,
                        "reps": 0,
                        "state": "waiting",
                    },
                    "feedback": {
                        "message": "No person detected",
                        "status": "waiting",
                    },
                }

                if detection["detected"]:
                    # Convert MediaPipe pixel landmarks to overlay format.
                    image_landmarks = detection["image_landmarks"]

                    for name in (
                        "left_shoulder", "right_shoulder",
                        "left_elbow", "right_elbow",
                        "left_wrist", "right_wrist",
                        "left_hip", "right_hip",
                        "left_knee", "right_knee",
                        "left_ankle", "right_ankle",
                    ):
                        point = image_landmarks.get(name)
                        if point and point["visibility"] >= 0.5:
                            landmarks[name] = (
                                int(point["x"]),
                                int(point["y"]),
                            )

                    # Use the left leg when all three landmarks are visible.
                    hip = image_landmarks.get("left_hip")
                    knee = image_landmarks.get("left_knee")
                    ankle = image_landmarks.get("left_ankle")

                    if all(
                        point and point["visibility"] >= 0.5
                        for point in (hip, knee, ankle)
                    ):
                        result = pipeline.process_landmarks(
                            (hip["x"], hip["y"]),
                            (knee["x"], knee["y"]),
                            (ankle["x"], ankle["y"]),
                        )
                    else:
                        result["feedback"]["message"] = (
                            "Keep your left hip, knee and ankle visible"
                        )

                display_frame = draw_pipeline_overlay(
                    frame, landmarks, result
                )
                cv2.imshow("AR Sports Coach", display_frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    except Exception as error:
        print(f"Live demo failed: {error}")

    finally:
        cv2.destroyAllWindows()
        print("AR Sports Coach stopped.")


if __name__ == "__main__":
    main()
