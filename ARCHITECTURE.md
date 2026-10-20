# AR Sports Coach — Architecture Contract

## 1. Project goal
Build an application that analyzes squat movements from camera input
and provides real-time visual coaching feedback.

## 2. Module responsibilities

- vision/: capture or process frames and detect body landmarks.
- analysis/: calculate joint angles, movement states, and repetitions.
- ai/: turn exercise metrics into understandable coaching feedback.
- integration/: coordinate the modules and produce a unified result.
- ar/: draw visual feedback and overlays.
- ui/: display application status and exercise information.
- config/: hold shared configuration.
- tests/: automated unit and integration tests.
- assets/: icons and model assets.

## 3. Initial data contracts

### Landmarks
Use a documented representation agreed upon with the vision module owner.
Each landmark must have a consistent coordinate format.
Missing landmarks must be handled explicitly.

### Exercise metrics
The analysis-to-coach interface initially uses a dictionary:
{
    "knee_angle": 90.0,
    "reps": 3,
    "state": "standing"
}

Values above are examples, not live measurements.
knee_angle may be None when unavailable.

### Coaching feedback
generate_feedback(metrics: dict) -> dict

Expected result:
{
    "message": "Keep going! Maintain controlled movement.",
    "status": "good"
}

Supported initial statuses:
- waiting
- good
- warning

These are prototype rules, not medical advice.

### Integration result
The integration pipeline should return a documented result
containing the available exercise metrics and coaching feedback.
Its final schema must be agreed upon before teammates depend on it.

## 4. Engineering rules
- Keep module responsibilities separate.
- Document public functions and their inputs/outputs.
- Handle missing or invalid measurements safely.
- Add tests for new behavior.
- Do not silently change shared interfaces.
- Run the full test suite before committing.
- Coordinate interface changes with affected teammates.

## 5. Current verification baseline
24 automated tests passed on Python 3.14.8.
Re-run tests after every significant change.

## 6. Open interface decisions
- Which pose detector and landmark format will vision use?
- Which side's knee will be analyzed?
- What exact result schema will integration expose?
- What inputs will the AR overlay and UI require?

