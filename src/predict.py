from pathlib import Path

from ultralytics import YOLO


DATASET_PATH = Path(
    "B:/Pos/IADT/data/stride-architecture-components-v1/data.yaml"
)

OUTPUT_PATH = Path("B:/Pos/IADT/training/runs")


def main() -> None:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Arquivo data.yaml não encontrado: {DATASET_PATH}"
        )

    model = YOLO("yolov8n.pt")

    model.train(
        data=str(DATASET_PATH),
        epochs=20,
        imgsz=640,
        batch=16,
        workers=8,
        device=0,
        project=str(OUTPUT_PATH),
        name="stride_architecture_detector",
        exist_ok=True,
    )


if __name__ == "__main__":
    main()