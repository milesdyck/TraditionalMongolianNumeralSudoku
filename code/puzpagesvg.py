import scribus
from pathlib import Path
import csv

FIRST_PUZZLE_PAGE = 1
LAST_PUZZLE_PAGE = 99
BASE_FRAME_NAME = "puz_num"

TARGET_FONT = "Charm Bold"
TARGET_SIZE = 14.0

SVG_DIR = Path(r"C:\Users\MilesIdeaPad\Documents\python\Processed")
LOOKUP_CSV = Path(r"C:\Users\MilesIdeaPad\Documents\python\page_dictionary.csv")

SVG_WIDTH = 4.167
SVG_HEIGHT = 4.167
SVG_X = 0.6665
SVG_Y = 1.9028


def is_target_frame(name):
    return name == BASE_FRAME_NAME or name.startswith(f"Copy of {BASE_FRAME_NAME}")


def set_frame_text(frame_name, text_value):
    if scribus.getTextLength(frame_name) > 0:
        scribus.deleteText(frame_name)
    scribus.insertText(text_value, 0, frame_name)
    scribus.setFont(TARGET_FONT, frame_name)
    scribus.setFontSize(TARGET_SIZE, frame_name)

def load_prefix_lookup():
    lookup = {}
    with open(LOOKUP_CSV, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            page_num = int(row["page"])
            prefix = row["prefix"].strip()
            lookup[page_num] = prefix
    return lookup

def find_svg_for_page(page_num, prefix_lookup):
    prefix = prefix_lookup.get(page_num)
    if prefix is None:
        return None

    matches = sorted(SVG_DIR.glob(f"{prefix}_*.svg"))
    if not matches:
        matches = sorted(SVG_DIR.glob(f"{prefix}_*.SVG"))
    if not matches:
        return None
    return matches[0]

def delete_existing_puzzle_svg(page_num):
    target_name = f"puzzle_svg_{page_num}"
    page_items = scribus.getPageItems()

    for item in page_items:
        obj_name = item[0]
        if obj_name == target_name:
            scribus.deleteObject(obj_name)
            return True

    return False


def main():
    if not scribus.haveDoc():
        scribus.messageBox("Error", "No Scribus document is open.")
        return

    if not SVG_DIR.exists():
        scribus.messageBox("Error", f"SVG folder not found:\n{SVG_DIR}")
        return

    if not LOOKUP_CSV.exists():
        scribus.messageBox("Error", f"Lookup CSV not found:\n{LOOKUP_CSV}")
        return

    prefix_lookup = load_prefix_lookup()

    original_unit = scribus.getUnit()
    scribus.setUnit(scribus.UNIT_INCHES)

    missing_pages = []
    missing_svgs = []

    try:
        for page_num in range(FIRST_PUZZLE_PAGE, LAST_PUZZLE_PAGE + 1):
            scribus.gotoPage(page_num)

            page_items = scribus.getPageItems()

            target_name = None
            for item in page_items:
                obj_name = item[0]
                if is_target_frame(obj_name):
                    target_name = obj_name
                    break

            if target_name is None:
                missing_pages.append(page_num)
            else:
                set_frame_text(target_name, str(page_num))

            svg_path = find_svg_for_page(page_num, prefix_lookup)
            if svg_path is None:
                missing_svgs.append(page_num)
                continue

            delete_existing_puzzle_svg(page_num)

            scribus.placeSVG(str(svg_path), SVG_X, SVG_Y)

            imported_name = f"puzzle_svg_{page_num}"
            scribus.setItemName(imported_name)
            scribus.sizeObject(SVG_WIDTH, SVG_HEIGHT, imported_name)
            scribus.moveObjectAbs(SVG_X, SVG_Y, imported_name)

        scribus.docChanged(True)
        scribus.redrawAll()

        messages = []
        if missing_pages:
            messages.append(
                "No puzzle-number frame found on page(s): "
                + ", ".join(map(str, missing_pages))
            )
        if missing_svgs:
            messages.append(
                "No matching SVG found for page(s): "
                + ", ".join(map(str, missing_svgs))
            )

        if messages:
            scribus.messageBox("Finished with warnings", "\n\n".join(messages))
        else:
            scribus.messageBox("Finished", "Puzzle numbers and SVGs inserted successfully.")

    finally:
        scribus.setUnit(original_unit)


if __name__ == "__main__":
    main()