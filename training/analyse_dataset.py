from collections import Counter
from pathlib import Path
import csv

import matplotlib.pyplot as plt


DATASET_PATH = Path("../data/dataset/architecture_dataset")
REPORT_PATH = Path("../reports/dataset")

CLASS_NAMES = {
    0: "user",
    1: "server",
    2: "process",
    3: "database",
    4: "storage",
    5: "load_balancer",
    6: "firewall",
    7: "external_system",
}


def count_labels(labels_path: Path) -> Counter[int]:
    counter: Counter[int] = Counter()

    for label_file in labels_path.glob("*.txt"):
        with label_file.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                class_id = int(line.split()[0])
                counter[class_id] += 1

    return counter


def count_images(images_path: Path) -> int:
    valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

    return sum(
        1
        for image_path in images_path.iterdir()
        if image_path.is_file()
        and image_path.suffix.lower() in valid_extensions
    )


def generate_class_distribution_chart(
    total_counter: Counter[int],
) -> None:
    class_names = [
        CLASS_NAMES[class_id]
        for class_id in CLASS_NAMES
    ]

    counts = [
        total_counter.get(class_id, 0)
        for class_id in CLASS_NAMES
    ]

    plt.figure(figsize=(10, 6))
    bars = plt.barh(class_names, counts)

    plt.xlabel("Quantidade de objetos")
    plt.ylabel("Classe")
    plt.title("Distribuição de objetos por classe")
    plt.grid(axis="x", linestyle="--", alpha=0.4)

    for bar, count in zip(bars, counts):
        plt.text(
            bar.get_width(),
            bar.get_y() + bar.get_height() / 2,
            f" {count}",
            va="center",
        )

    plt.tight_layout()
    plt.savefig(
        REPORT_PATH / "class_distribution.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()


def generate_train_val_chart(
    train_images: int,
    val_images: int,
) -> None:
    labels = ["Treino", "Validação"]
    values = [train_images, val_images]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, values)

    plt.ylabel("Quantidade de imagens")
    plt.title("Distribuição de imagens entre treino e validação")
    plt.grid(axis="y", linestyle="--", alpha=0.4)

    for bar, value in zip(bars, values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value}",
            ha="center",
            va="bottom",
        )

    plt.tight_layout()
    plt.savefig(
        REPORT_PATH / "train_val_distribution.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()


def generate_percentage_chart(
    total_counter: Counter[int],
) -> None:
    labels = []
    values = []

    for class_id, class_name in CLASS_NAMES.items():
        count = total_counter.get(class_id, 0)

        if count > 0:
            labels.append(class_name)
            values.append(count)

    plt.figure(figsize=(9, 7))
    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
    )

    plt.title("Percentual de objetos por classe")
    plt.tight_layout()
    plt.savefig(
        REPORT_PATH / "class_percentage.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()


def generate_csv(
    train_counter: Counter[int],
    val_counter: Counter[int],
) -> None:
    total_counter = train_counter + val_counter
    total_objects = sum(total_counter.values())

    csv_path = REPORT_PATH / "class_distribution.csv"

    with csv_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.writer(file)

        writer.writerow(
            [
                "class_id",
                "class_name",
                "train_objects",
                "validation_objects",
                "total_objects",
                "percentage",
            ]
        )

        for class_id, class_name in CLASS_NAMES.items():
            train_count = train_counter.get(class_id, 0)
            val_count = val_counter.get(class_id, 0)
            total_count = total_counter.get(class_id, 0)

            percentage = (
                total_count / total_objects * 100
                if total_objects > 0
                else 0
            )

            writer.writerow(
                [
                    class_id,
                    class_name,
                    train_count,
                    val_count,
                    total_count,
                    f"{percentage:.2f}",
                ]
            )


def generate_summary(
    train_counter: Counter[int],
    val_counter: Counter[int],
    train_images: int,
    val_images: int,
) -> None:
    total_counter = train_counter + val_counter

    total_objects = sum(total_counter.values())
    total_images = train_images + val_images

    most_common = total_counter.most_common(1)

    least_common = sorted(
        [
            (class_id, total_counter.get(class_id, 0))
            for class_id in CLASS_NAMES
        ],
        key=lambda item: item[1],
    )

    most_frequent_name = (
        CLASS_NAMES[most_common[0][0]]
        if most_common
        else "N/A"
    )

    least_frequent_name = (
        CLASS_NAMES[least_common[0][0]]
        if least_common
        else "N/A"
    )

    summary = f"""
RESUMO DO DATASET
=================

Imagens totais............... {total_images}
Imagens de treino............ {train_images}
Imagens de validação......... {val_images}

Objetos totais............... {total_objects}
Quantidade de classes........ {len(CLASS_NAMES)}

Classe mais frequente........ {most_frequent_name}
Classe menos frequente....... {least_frequent_name}

DISTRIBUIÇÃO DAS CLASSES
========================
"""

    for class_id, class_name in CLASS_NAMES.items():
        train_count = train_counter.get(class_id, 0)
        val_count = val_counter.get(class_id, 0)
        total_count = total_counter.get(class_id, 0)

        percentage = (
            total_count / total_objects * 100
            if total_objects > 0
            else 0
        )

        summary += (
            f"\n{class_id} - {class_name}\n"
            f"  Treino:     {train_count}\n"
            f"  Validação:  {val_count}\n"
            f"  Total:      {total_count}\n"
            f"  Percentual: {percentage:.2f}%\n"
        )

    summary_path = REPORT_PATH / "dataset_summary.txt"

    summary_path.write_text(
        summary.strip(),
        encoding="utf-8",
    )


def print_results(
    train_counter: Counter[int],
    val_counter: Counter[int],
    train_images: int,
    val_images: int,
) -> None:
    total_counter = train_counter + val_counter
    total_objects = sum(total_counter.values())

    print("\nAnálise concluída")
    print("-----------------")
    print(f"Imagens de treino: {train_images}")
    print(f"Imagens de validação: {val_images}")
    print(f"Total de imagens: {train_images + val_images}")
    print(f"Total de objetos: {total_objects}")

    print("\nDistribuição das classes:")

    for class_id, class_name in CLASS_NAMES.items():
        count = total_counter.get(class_id, 0)

        percentage = (
            count / total_objects * 100
            if total_objects > 0
            else 0
        )

        print(
            f"{class_id} - {class_name}: "
            f"{count} ({percentage:.2f}%)"
        )

    print(f"\nRelatórios gerados em: {REPORT_PATH}")


def main() -> None:
    train_labels_path = DATASET_PATH / "labels" / "train"
    val_labels_path = DATASET_PATH / "labels" / "val"

    train_images_path = DATASET_PATH / "images" / "train"
    val_images_path = DATASET_PATH / "images" / "val"

    required_paths = [
        train_labels_path,
        val_labels_path,
        train_images_path,
        val_images_path,
    ]

    for path in required_paths:
        if not path.exists():
            raise FileNotFoundError(
                f"Pasta não encontrada: {path}"
            )

    REPORT_PATH.mkdir(
        parents=True,
        exist_ok=True,
    )

    train_counter = count_labels(train_labels_path)
    val_counter = count_labels(val_labels_path)

    train_images = count_images(train_images_path)
    val_images = count_images(val_images_path)

    total_counter = train_counter + val_counter

    generate_class_distribution_chart(total_counter)
    generate_train_val_chart(train_images, val_images)
    generate_percentage_chart(total_counter)

    generate_csv(
        train_counter,
        val_counter,
    )

    generate_summary(
        train_counter,
        val_counter,
        train_images,
        val_images,
    )

    print_results(
        train_counter,
        val_counter,
        train_images,
        val_images,
    )


if __name__ == "__main__":
    main()