from pathlib import Path

from ultralytics import YOLO


DATA_YAML = Path("../data/stride-architecture-components-v1/data.yaml")
OUTPUT_PATH = Path("../training/runs/detections")


def main() -> None:
    if not DATA_YAML.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {DATA_YAML}"
        )

    model = YOLO("yolov8n.pt")

    model.train(
        data=str(DATA_YAML),
        epochs=20,
        imgsz=640,
        batch=8,
        project=str(OUTPUT_PATH),
        name="stride_architecture_detector",
        patience=5,
        workers=4,
        device=0,
)


if __name__ == "__main__":
    main()