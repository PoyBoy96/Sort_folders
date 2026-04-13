import argparse
import shutil
import sys
from pathlib import Path
from datetime import datetime

from PIL import Image

try:
    import cv2
except ImportError:
    cv2 = None


VIDEO_EXTENSIONS = {
    ".mp4", ".mov", ".avi", ".mkv", ".wmv", ".m4v", ".mpg", ".mpeg", ".webm", ".3gp"
}

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp", ".heic"
}

HI_RES_WIDTH = 1920
HI_RES_HEIGHT = 1080


def is_video(file_path: Path) -> bool:
    return file_path.suffix.lower() in VIDEO_EXTENSIONS


def is_image(file_path: Path) -> bool:
    return file_path.suffix.lower() in IMAGE_EXTENSIONS


def get_image_dimensions(file_path: Path):
    try:
        with Image.open(file_path) as img:
            return img.width, img.height
    except Exception as e:
        return None


def get_video_dimensions(file_path: Path):
    if cv2 is None:
        return None

    try:
        cap = cv2.VideoCapture(str(file_path))
        if not cap.isOpened():
            return None

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()

        if width <= 0 or height <= 0:
            return None

        return width, height
    except Exception:
        return None


def is_hi_res(width: int, height: int) -> bool:
    return width >= HI_RES_WIDTH and height >= HI_RES_HEIGHT


def classify_submission_folder(folder_path: Path):
    has_video = False
    has_landscape_image = False
    has_hi_res = False

    all_files = [p for p in folder_path.rglob("*") if p.is_file()]

    for file_path in all_files:
        if is_video(file_path):
            has_video = True
            dims = get_video_dimensions(file_path)
            if dims and is_hi_res(*dims):
                has_hi_res = True

        elif is_image(file_path):
            dims = get_image_dimensions(file_path)
            if dims:
                width, height = dims

                if width > height:
                    has_landscape_image = True

                if is_hi_res(width, height):
                    has_hi_res = True

    if has_video:
        category = "Videos"
    elif has_landscape_image:
        category = "Landscape"
    else:
        category = "Portrait"

    resolution_group = "Hi Res" if has_hi_res else "Low Res"
    return category, resolution_group


def safe_destination(base_output: Path, category: str, resolution_group: str, folder_name: str) -> Path:
    destination = base_output / category / resolution_group / folder_name

    if not destination.exists():
        return destination

    counter = 2
    while True:
        candidate = base_output / category / resolution_group / f"{folder_name}_{counter}"
        if not candidate.exists():
            return candidate
        counter += 1


def create_log_file(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = output_root.parent / f"sort_log_{timestamp}.txt"
    return log_path


def log_line(log_file, message: str):
    print(message)
    log_file.write(message + "\n")


def move_submission_folders(input_root: Path, output_root: Path):
    log_path = create_log_file(output_root)

    with open(log_path, "w", encoding="utf-8") as log_file:
        log_line(log_file, f"=== SORT RUN {datetime.now()} ===\n")
        log_line(log_file, f"Input: {input_root}")
        log_line(log_file, f"Output: {output_root}\n")

        submission_folders = [p for p in input_root.iterdir() if p.is_dir()]

        if not submission_folders:
            log_line(log_file, "No submission folders found.")
            return

        for folder_path in submission_folders:
            log_line(log_file, f"\nChecking: {folder_path.name}")

            try:
                category, resolution_group = classify_submission_folder(folder_path)
                destination = safe_destination(
                    output_root,
                    category,
                    resolution_group,
                    folder_path.name
                )

                destination.parent.mkdir(parents=True, exist_ok=True)

                log_line(log_file, f"Category: {category}")
                log_line(log_file, f"Resolution: {resolution_group}")
                log_line(log_file, f"Destination: {destination}")

                shutil.move(str(folder_path), str(destination))

                log_line(log_file, "Status: SUCCESS")

            except Exception as e:
                log_line(log_file, f"Status: ERROR - {e}")

        log_line(log_file, "\n=== END RUN ===")

    print(f"\nLog saved to: {log_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Sort submission folders into Videos, Landscape, or Portrait, then Hi Res or Low Res."
    )
    parser.add_argument("input_folder")
    parser.add_argument("output_folder")

    args = parser.parse_args()

    input_root = Path(args.input_folder).resolve()
    output_root = Path(args.output_folder).resolve()

    try:
        move_submission_folders(input_root, output_root)
        print("\nDone.")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()