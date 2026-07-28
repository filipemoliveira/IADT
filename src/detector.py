from pathlib import Path

from ultralytics import YOLO

from models import ArchitectureComponent


MODEL_PATH = Path(
    "models/architecture_detector/weights/best.pt"
)


def detect_components(
    image_path: str,
    confidence: float = 0.40,
) -> list[ArchitectureComponent]:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"YOLO model not found: {MODEL_PATH}"
        )

    image = Path(image_path)

    if not image.exists():
        raise FileNotFoundError(
            f"Image not found: {image}"
        )

    model = YOLO(str(MODEL_PATH))

    results = model.predict(
        source=str(image),
        conf=confidence,
        verbose=False,
    )

    components: list[ArchitectureComponent] = []
    seen_components: set[str] = set()

    for result in results:
        if result.boxes is None:
            continue

        for box in result.boxes:
            class_id = int(box.cls.item())
            class_name = result.names[class_id]

            normalized_name = (
                class_name
                .strip()
                .lower()
            )

            if normalized_name in seen_components:
                continue

            seen_components.add(normalized_name)

            components.append(
                ArchitectureComponent(
                    name=class_name,
                    component_type=class_name,
                )
            )

    if not components:
        raise ValueError(
            "No architecture components were detected."
        )

    return components