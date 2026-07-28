from pathlib import Path
import random
import shutil
import xml.etree.ElementTree as ET


SOURCE_PATH = Path("../data/dataset/dataset_augmented")
OUTPUT_PATH = Path("../data/dataset/architecture_dataset")

TRAIN_SPLIT = 0.8
RANDOM_SEED = 42

CLASS_MAPPING = {
    # Server / Compute
    "gcp_compute_engine": "server",
    "azure_virtual_machine": "server",
    "aws_ec2_instance": "server",

    # Process / Application
    "aws_lambda": "process",
    "gcp_cloud_run": "process",
    "azure_function_apps": "process",
    "azure_app_services": "process",

    # Database
    "azure_sql_database": "database",
    "gcp_cloud_sql": "database",
    "aws_dynamodb_table": "database",
    "azure_cosmos_db": "database",

    # Storage
    "azure_storage_accounts": "storage",
    "gcp_cloud_storage": "storage",
    "aws_simple_storage_service_bucket": "storage",
    "aws_amazon_elastic_block_store": "storage",

    # Load balancer
    "gcp_cloud_load_balancing": "load_balancer",
    "azure_load_balancers": "load_balancer",
    "aws_elastic_load_balancing_application_load_balancer": "load_balancer",
    "aws_elastic_load_balancing_network_load_balancer": "load_balancer",

    # Firewall / Security boundary
    "azure_network_security_groups": "firewall",

    # External managed services
    "azure_openai": "external_system",
    "gcp_vertex_ai": "external_system",
}

YOLO_CLASSES = {
    "user": 0,
    "server": 1,
    "process": 2,
    "database": 3,
    "storage": 4,
    "load_balancer": 5,
    "firewall": 6,
    "external_system": 7,
}


def create_directories() -> None:
    for split in ("train", "val"):
        (OUTPUT_PATH / "images" / split).mkdir(parents=True, exist_ok=True)
        (OUTPUT_PATH / "labels" / split).mkdir(parents=True, exist_ok=True)


def find_image(xml_path: Path) -> Path | None:
    for extension in (".png", ".jpg", ".jpeg"):
        image_path = xml_path.with_suffix(extension)

        if image_path.exists():
            return image_path

    return None


def convert_box(
    image_width: int,
    image_height: int,
    xmin: float,
    ymin: float,
    xmax: float,
    ymax: float,
) -> tuple[float, float, float, float]:
    box_width = xmax - xmin
    box_height = ymax - ymin

    center_x = xmin + box_width / 2
    center_y = ymin + box_height / 2

    return (
        center_x / image_width,
        center_y / image_height,
        box_width / image_width,
        box_height / image_height,
    )


def convert_annotation(xml_path: Path) -> list[str]:
    root = ET.parse(xml_path).getroot()

    size = root.find("size")

    if size is None:
        return []

    image_width = int(size.findtext("width", "0"))
    image_height = int(size.findtext("height", "0"))

    if image_width <= 0 or image_height <= 0:
        return []

    labels: list[str] = []

    for obj in root.findall("object"):
        original_class = obj.findtext("name", "").strip()
        mapped_class = CLASS_MAPPING.get(original_class)

        if mapped_class is None:
            continue

        box = obj.find("bndbox")

        if box is None:
            continue

        xmin = float(box.findtext("xmin", "0"))
        ymin = float(box.findtext("ymin", "0"))
        xmax = float(box.findtext("xmax", "0"))
        ymax = float(box.findtext("ymax", "0"))

        center_x, center_y, width, height = convert_box(
            image_width,
            image_height,
            xmin,
            ymin,
            xmax,
            ymax,
        )

        class_id = YOLO_CLASSES[mapped_class]

        labels.append(
            f"{class_id} "
            f"{center_x:.6f} "
            f"{center_y:.6f} "
            f"{width:.6f} "
            f"{height:.6f}"
        )

    return labels


def save_sample(xml_path: Path, split: str) -> bool:
    image_path = find_image(xml_path)

    if image_path is None:
        return False

    labels = convert_annotation(xml_path)

    if not labels:
        return False

    destination_image = OUTPUT_PATH / "images" / split / image_path.name
    destination_label = OUTPUT_PATH / "labels" / split / f"{image_path.stem}.txt"

    shutil.copy2(image_path, destination_image)
    destination_label.write_text("\n".join(labels), encoding="utf-8")

    return True


def main() -> None:
    create_directories()

    xml_files = list(SOURCE_PATH.glob("*.xml"))

    if not xml_files:
        raise FileNotFoundError(
            f"Nenhum arquivo XML encontrado em: {SOURCE_PATH}"
        )

    random.seed(RANDOM_SEED)
    random.shuffle(xml_files)

    split_index = int(len(xml_files) * TRAIN_SPLIT)

    train_files = xml_files[:split_index]
    val_files = xml_files[split_index:]

    train_count = sum(save_sample(xml_file, "train") for xml_file in train_files)
    val_count = sum(save_sample(xml_file, "val") for xml_file in val_files)

    print(f"XMLs encontrados: {len(xml_files)}")
    print(f"Imagens de treino geradas: {train_count}")
    print(f"Imagens de validação geradas: {val_count}")


if __name__ == "__main__":
    main()