import re
import xml.etree.ElementTree as ET
from pathlib import Path

DIGIT_MAP = {
    "1": "᠑",
    "2": "᠒",
    "3": "᠓",
    "4": "᠔",
    "5": "᠕",
    "6": "᠖",
    "7": "᠗",
    "8": "᠘",
    "9": "᠙",
}

FONT_FAMILY = "Khatan"
FONT_SIZE_REDUCTION = 2.0
STROKE_WIDTH = "0.04px"
Y_SHIFT = -0.2

INPUT_DIR = Path(r"C:\Users\MilesIdeaPad\Documents\python\Sudoku_SVG_0_Solutions")
OUTPUT_DIR = Path(r"C:\Users\MilesIdeaPad\Documents\python\Swapped_Solutions")


def parse_style(style_string: str) -> dict:
    styles = {}
    for item in style_string.split(";"):
        item = item.strip()
        if not item or ":" not in item:
            continue
        key, value = item.split(":", 1)
        styles[key.strip()] = value.strip()
    return styles


def style_to_string(styles: dict) -> str:
    return ";".join(f"{k}:{v}" for k, v in styles.items())


def reduce_size_value(size_value: str, reduction: float) -> str:
    match = re.fullmatch(r"\s*([0-9]*\.?[0-9]+)\s*([a-zA-Z%]*)\s*", size_value)
    if not match:
        return size_value

    value = float(match.group(1))
    unit = match.group(2)
    new_value = max(1.0, value - reduction)

    if new_value.is_integer():
        return f"{int(new_value)}{unit}"
    return f"{new_value}{unit}"


def shift_coordinate(value: str, shift: float) -> str:
    match = re.fullmatch(r"\s*([0-9]*\.?[0-9]+)\s*", value)
    if not match:
        return value

    new_value = float(match.group(1)) + shift
    if new_value.is_integer():
        return str(int(new_value))
    return str(new_value)


def process_svg_file(input_path: Path, output_path: Path) -> int:
    tree = ET.parse(input_path)
    root = tree.getroot()

    replacements = 0

    for elem in root.iter():
        tag = elem.tag.lower()
        if not tag.endswith("text"):
            continue

        if elem.text is None:
            continue

        original_text = elem.text.strip()
        if original_text not in DIGIT_MAP:
            continue

        elem.text = DIGIT_MAP[original_text]
        replacements += 1

        style_dict = parse_style(elem.get("style", ""))

        style_dict["font-family"] = FONT_FAMILY
        style_dict["fill"] = "#000000"
        style_dict["fill-opacity"] = "1"
        style_dict["stroke"] = "#000000"
        style_dict["stroke-width"] = STROKE_WIDTH
        style_dict["stroke-opacity"] = "1"

        if "font-size" in style_dict:
            style_dict["font-size"] = reduce_size_value(
                style_dict["font-size"],
                FONT_SIZE_REDUCTION
            )

        elem.set("style", style_to_string(style_dict))

        elem.set("font-family", FONT_FAMILY)
        elem.set("fill", "#000000")
        elem.set("fill-opacity", "1")
        elem.set("stroke", "#000000")
        elem.set("stroke-width", STROKE_WIDTH)
        elem.set("stroke-opacity", "1")

        if "font-size" in elem.attrib:
            elem.set(
                "font-size",
                reduce_size_value(elem.get("font-size", ""), FONT_SIZE_REDUCTION)
            )

        if "y" in elem.attrib:
            elem.set("y", shift_coordinate(elem.get("y", ""), Y_SHIFT))

    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    return replacements


def main() -> None:
    if not INPUT_DIR.exists():
        raise FileNotFoundError(f"Input folder not found: {INPUT_DIR}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    svg_files = sorted(INPUT_DIR.glob("*.SVG"))

    if not svg_files:
        svg_files = sorted(INPUT_DIR.glob("*.svg"))

    if not svg_files:
        print("No SVG files found.")
        return

    total_files = 0
    total_replacements = 0

    for input_path in svg_files:
        stem = input_path.stem  # e.g. "#1"
        output_name = f"{stem}_swapped.svg"
        output_path = OUTPUT_DIR / output_name

        replacements = process_svg_file(input_path, output_path)

        total_files += 1
        total_replacements += replacements

        print(f"Processed {input_path.name} -> {output_path.name} ({replacements} replacements)")

    print()
    print(f"Done. Processed {total_files} files.")
    print(f"Total digit replacements: {total_replacements}")
    print(f"Output folder: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()