import scribus
from pathlib import Path
import csv
import math

# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

SVG_DIR = Path(r"C:\Users\MilesIdeaPad\Documents\python\Processed_Solutions")
LOOKUP_CSV = Path(r"C:\Users\MilesIdeaPad\Documents\python\page_dictionary.csv")

# ---------------------------------------------------------------------
# Layout settings (inches)
# ---------------------------------------------------------------------

SOL_WIDTH = 1.85
SOL_HEIGHT = 1.85

POSITIONS = [
    (0.7855, 1.865),   # slot 1
    (2.865, 1.865),    # slot 2
    (0.7855, 4.4375),  # slot 3
    (2.865, 4.4375),   # slot 4
]

TEXT_FRAME_BASES = [
    "sol_num_1",
    "sol_num_2",
    "sol_num_3",
    "sol_num_4",
]

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def load_solution_lookup():
    rows = []
    with open(LOOKUP_CSV, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            page_num = int(row["page"])
            prefix = row["prefix"].strip()
            rows.append({"page": page_num, "prefix": prefix})
    rows.sort(key=lambda x: x["page"])
    return rows


def is_matching_frame_name(actual_name, base_name):
    return actual_name == base_name or actual_name.startswith(f"Copy of {base_name}")


def find_text_frame_on_page(base_name):
    page_items = scribus.getPageItems()
    for item in page_items:
        obj_name = item[0]
        if is_matching_frame_name(obj_name, base_name):
            return obj_name
    return None


def set_frame_text(frame_name, text_value):
    if scribus.getTextLength(frame_name) > 0:
        scribus.deleteText(frame_name)
    scribus.insertText(str(text_value), 0, frame_name)


def clear_frame_text(frame_name):
    if scribus.getTextLength(frame_name) > 0:
        scribus.deleteText(frame_name)


def find_solution_svg(prefix):
    candidates = [
        SVG_DIR / f"{prefix}_solved_swapped_processed.SVG",
        SVG_DIR / f"{prefix}_solved_swapped_processed.svg",
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def delete_existing_solution_svg(page_num, slot_num):
    target_name = f"solution_svg_{page_num}_{slot_num}"
    page_items = scribus.getPageItems()
    for item in page_items:
        obj_name = item[0]
        if obj_name == target_name:
            scribus.deleteObject(obj_name)
            return True
    return False


def place_solution_svg(svg_path, page_num, slot_num, xpos, ypos):
    delete_existing_solution_svg(page_num, slot_num)

    scribus.placeSVG(str(svg_path), xpos, ypos)

    imported_name = f"solution_svg_{page_num}_{slot_num}"
    scribus.setItemName(imported_name)
    scribus.sizeObject(SOL_WIDTH, SOL_HEIGHT, imported_name)
    scribus.moveObjectAbs(xpos, ypos, imported_name)


def clear_unused_slot(page_num, slot_num, base_frame_name):
    frame_name = find_text_frame_on_page(base_frame_name)
    if frame_name is not None:
        clear_frame_text(frame_name)

    delete_existing_solution_svg(page_num, slot_num)


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

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

    solution_rows = load_solution_lookup()
    total_puzzles = len(solution_rows)
    required_pages = math.ceil(total_puzzles / 4)

    doc_pages = scribus.pageCount()
    if doc_pages < required_pages:
        scribus.messageBox(
            "Error",
            f"Not enough Scribus pages.\n"
            f"Need {required_pages} solution pages for {total_puzzles} puzzles,\n"
            f"but the document only has {doc_pages} pages."
        )
        return

    original_unit = scribus.getUnit()
    scribus.setUnit(scribus.UNIT_INCHES)

    missing_frames = []
    missing_svgs = []

    try:
        for scribus_page in range(1, required_pages + 1):
            scribus.gotoPage(scribus_page)

            start_idx = (scribus_page - 1) * 4
            end_idx = min(start_idx + 4, total_puzzles)
            page_rows = solution_rows[start_idx:end_idx]

            # Fill used slots
            for slot_idx, row in enumerate(page_rows, start=1):
                puzzle_page_number = row["page"]
                prefix = row["prefix"]

                frame_base = TEXT_FRAME_BASES[slot_idx - 1]
                frame_name = find_text_frame_on_page(frame_base)

                if frame_name is None:
                    missing_frames.append(f"page {scribus_page}, {frame_base}")
                else:
                    set_frame_text(frame_name, puzzle_page_number)

                svg_path = find_solution_svg(prefix)
                if svg_path is None:
                    missing_svgs.append(f"page {scribus_page}, prefix {prefix}")
                else:
                    xpos, ypos = POSITIONS[slot_idx - 1]
                    place_solution_svg(svg_path, scribus_page, slot_idx, xpos, ypos)

            # Clear unused slots on the last page, if any
            for slot_idx in range(len(page_rows) + 1, 5):
                frame_base = TEXT_FRAME_BASES[slot_idx - 1]
                clear_unused_slot(scribus_page, slot_idx, frame_base)

        scribus.docChanged(True)
        scribus.redrawAll()

        messages = []
        if missing_frames:
            messages.append(
                "Missing text frames:\n" + "\n".join(missing_frames)
            )
        if missing_svgs:
            messages.append(
                "Missing solution SVGs:\n" + "\n".join(missing_svgs)
            )

        if messages:
            scribus.messageBox("Finished with warnings", "\n\n".join(messages))
        else:
            scribus.messageBox("Finished", "Solutions inserted successfully.")

    finally:
        scribus.setUnit(original_unit)


if __name__ == "__main__":
    main()