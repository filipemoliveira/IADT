from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import torch
from ultralytics import YOLO


DATA_YAML = Path("D:/Pos/IADT/data/stride-architecture-components-v1")
OUTPUT_PATH = Path("D:/Pos/IADT/training/runs/architecture_detection")
RUN_NAME = "stride_architecture_detector"


def plot_metric(
    dataframe: pd.DataFrame,
    columns: list[str],
    title: str,
    filename: Path,
    ylabel: str,
) -> None:
    """
    Gera um gráfico acumulado com uma ou mais métricas.
    """

    available_columns = [
        column for column in columns if column in dataframe.columns
    ]

    if not available_columns:
        return

    plt.figure(figsize=(10, 6))

    for column in available_columns:
        plt.plot(
            dataframe["epoch"],
            dataframe[column],
            marker="o",
            markersize=3,
            label=column.strip(),
        )

    plt.title(title)
    plt.xlabel("Época")
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    filename.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(filename, dpi=150)
    plt.close()


def generate_epoch_plots(trainer) -> None:
    """
    Callback executado ao final de cada época.

    Cria uma pasta específica para a época e gera gráficos
    contendo a evolução acumulada do treinamento.
    """

    epoch_number = trainer.epoch + 1
    results_csv = Path(trainer.csv)

    if not results_csv.exists():
        print(
            f"[Plots] results.csv ainda não disponível "
            f"na época {epoch_number}."
        )
        return

    try:
        dataframe = pd.read_csv(results_csv)

        # Remove espaços dos nomes das colunas.
        dataframe.columns = [
            column.strip() for column in dataframe.columns
        ]

        epoch_folder = (
            Path(trainer.save_dir)
            / "epoch_plots"
            / f"epoch_{epoch_number:03d}"
        )

        epoch_folder.mkdir(parents=True, exist_ok=True)

        plot_metric(
            dataframe=dataframe,
            columns=[
                "train/box_loss",
                "train/cls_loss",
                "train/dfl_loss",
            ],
            title=f"Perdas de treinamento até a época {epoch_number}",
            filename=epoch_folder / "train_losses.png",
            ylabel="Loss",
        )

        plot_metric(
            dataframe=dataframe,
            columns=[
                "val/box_loss",
                "val/cls_loss",
                "val/dfl_loss",
            ],
            title=f"Perdas de validação até a época {epoch_number}",
            filename=epoch_folder / "validation_losses.png",
            ylabel="Loss",
        )

        plot_metric(
            dataframe=dataframe,
            columns=[
                "metrics/precision(B)",
                "metrics/recall(B)",
            ],
            title=f"Precision e Recall até a época {epoch_number}",
            filename=epoch_folder / "precision_recall.png",
            ylabel="Valor",
        )

        plot_metric(
            dataframe=dataframe,
            columns=[
                "metrics/mAP50(B)",
                "metrics/mAP50-95(B)",
            ],
            title=f"mAP até a época {epoch_number}",
            filename=epoch_folder / "map_metrics.png",
            ylabel="mAP",
        )

        plot_metric(
            dataframe=dataframe,
            columns=[
                "lr/pg0",
                "lr/pg1",
                "lr/pg2",
            ],
            title=f"Learning rate até a época {epoch_number}",
            filename=epoch_folder / "learning_rate.png",
            ylabel="Learning rate",
        )

        print(
            f"[Plots] Gráficos da época {epoch_number} salvos em: "
            f"{epoch_folder}"
        )

    except Exception as error:
        # O erro dos gráficos não interrompe o treinamento.
        print(
            f"[Plots] Não foi possível gerar os gráficos "
            f"da época {epoch_number}: {error}"
        )


def main() -> None:
    if not DATA_YAML.exists():
        raise FileNotFoundError(
            f"Arquivo data.yaml não encontrado: "
            f"{DATA_YAML.resolve()}"
        )

    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("CUDA não encontrada. O treinamento usará CPU.")

    model = YOLO("yolov8n.pt")

    # Registra o callback para executar após cada época completa.
    model.add_callback(
        "on_fit_epoch_end",
        generate_epoch_plots,
    )

    model.train(
        data=str(DATA_YAML),
        epochs=20,
        imgsz=640,
        batch=8,
        project=str(OUTPUT_PATH),
        name=RUN_NAME,
        patience=5,
        workers=4,
        device=0,
        amp=True,
        exist_ok=True,
        plots=True,
    )


if __name__ == "__main__":
    main()