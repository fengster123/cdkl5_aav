"""Export the embedded report screenshots from **every** image-bearing tab.

The first extraction pass exported only the consolidated tab (490 of the workbook's
1,718 images), so children who submitted in 2025-01..2026-09 were invisible. This
module walks every tab in :func:`workbook_sheets.ordered_sheets` and writes the
images that are not already on disk.

De-duplication is by **content hash**, not by name or row:

* the consolidated tab's 490 images are already in ``screenshots/``; each one is
  registered by hash and reported with ``status="existing"`` (nothing rewritten);
* ``(副本)`` and ``20241201-20241231`` are earlier snapshots of the same
  submissions, so their images collide by hash and get ``status="duplicate"`` with
  ``dup_of`` naming the file that already holds them;
* anything genuinely new is written to ``screenshots_extra/`` with a sheet-prefixed
  name so the OCR pass can tell the tabs apart.

Output ``blind_ocr/image_manifest.csv`` has one row per embedded image::

    sheet, slug, row, col, name, sha1, ext, filename, status, dup_of

Run from the ``cdkl5_aav`` folder::

    python -m projects.chinese_mutations_survey.export_screenshots
"""

from __future__ import annotations

import argparse
import hashlib
import io
import re
from pathlib import Path

import openpyxl
import pandas as pd
from PIL import Image

from projects.chinese_mutations_survey.workbook_sheets import (
    COL_NAME,
    MASTER,
    RAW_XLSX,
    ordered_sheets,
    sheet_slug,
)

BASE = Path(__file__).resolve().parent
EXISTING = BASE / "screenshots"
EXTRA = BASE / "screenshots_extra"
MANIFEST = BASE / "blind_ocr" / "image_manifest.csv"

_BAD_NAME_CHARS = re.compile(r'[\\/:*?"<>|\s]+')


def _safe_name(name: str) -> str:
    """Filename-safe child name; CJK is kept, punctuation and spaces are dropped."""
    return _BAD_NAME_CHARS.sub("", name)[:20]


def _existing_registry() -> dict[str, str]:
    """sha1 -> filename for screenshots already extracted by the first pass."""
    reg: dict[str, str] = {}
    for path in sorted(EXISTING.glob("*")):
        if path.is_file():
            reg.setdefault(hashlib.sha1(path.read_bytes()).hexdigest(), path.name)
    return reg


def _fingerprint(blob: bytes) -> list[int] | None:
    """16x16 greyscale fingerprint, used only when the bytes differ.

    The first extraction pass wrote 13 large PNGs out as re-encoded ``.jpeg``, so
    those images are already on disk under a different byte hash. Comparing a
    coarse greyscale thumbnail identifies them without re-OCRing the same report.
    """
    try:
        img = Image.open(io.BytesIO(blob)).convert("L").resize((16, 16))
    except Exception:
        return None
    return list(img.getdata())


def _same_picture(a: list[int], b: list[int], tol: float = 4.0) -> bool:
    return bool(a) and bool(b) and sum(abs(x - y) for x, y in zip(a, b)) / len(a) <= tol


def _unique_path(outdir: Path, stem: str, ext: str) -> Path:
    path = outdir / f"{stem}.{ext}"
    n = 2
    while path.exists():
        path = outdir / f"{stem}__{n}.{ext}"
        n += 1
    return path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(EXTRA), help="folder for new images")
    ap.add_argument("--only-sheets", default="", help="comma-separated slugs (omitted = all)")
    ap.add_argument("--limit", type=int, default=0, help="stop after N new images (smoke test)")
    ap.add_argument("--dry-run", action="store_true", help="report only, write no image files")
    args, _ = ap.parse_known_args()
    outdir = Path(args.out)
    only = {s.strip() for s in args.only_sheets.split(",") if s.strip()}

    if not RAW_XLSX.exists():
        raise SystemExit(f"missing workbook {RAW_XLSX}")
    if not args.dry_run:
        outdir.mkdir(parents=True, exist_ok=True)

    seen = _existing_registry()
    disk_reg = dict(seen)
    used_disk: set[str] = set()
    print(f"images already on disk: {len(seen)} (hashes registered)")

    wb = openpyxl.load_workbook(RAW_XLSX)
    frames: dict[str, pd.DataFrame] = {}
    rows: list[dict] = []
    pending: list[tuple[dict, bytes]] = []
    written = 0

    for sheet in ordered_sheets(wb.sheetnames):
        if only and sheet_slug(sheet) not in only:
            continue
        ws = wb[sheet]
        images = list(getattr(ws, "_images", []))
        if not images:
            continue
        frames[sheet] = pd.read_excel(RAW_XLSX, sheet_name=sheet, header=None, dtype=object)
        vals = frames[sheet]
        for im in images:
            try:
                row_1b = im.anchor._from.row + 1
                col_1b = im.anchor._from.col + 1
            except Exception:
                row_1b = col_1b = -1
            blob = im._data()
            sha = hashlib.sha1(blob).hexdigest()
            try:
                ext = (Image.open(io.BytesIO(blob)).format or "PNG").lower()
                ext = "jpeg" if ext in {"jpg", "jpeg"} else ext
            except Exception:
                ext = "png"

            name = ""
            if 0 < row_1b <= len(vals) and vals.shape[1] > COL_NAME:
                cell = vals.iat[row_1b - 1, COL_NAME]
                name = "" if pd.isna(cell) else str(cell).strip()

            rec = {
                "sheet": sheet,
                "slug": sheet_slug(sheet),
                "row": row_1b,
                "col": col_1b,
                "name": name,
                "sha1": sha,
                "ext": ext,
            }
            if sha in seen:
                owner = seen[sha]
                rec["filename"] = owner
                rec["status"] = "existing" if sheet == MASTER else "duplicate"
                rec["dup_of"] = None if sheet == MASTER else owner
                rows.append(rec)
                if sha in disk_reg:
                    used_disk.add(sha)
                continue

            stem = f"{rec['slug']}_row{row_1b:03d}_c{col_1b:02d}_{_safe_name(name)}".rstrip("_")
            if args.dry_run:
                rec["filename"] = f"{stem}.{ext}"
                seen[sha] = rec["filename"]  # so a later tab cannot count it again
            else:
                path = _unique_path(outdir, stem, ext)
                path.write_bytes(blob)
                rec["filename"] = path.name
                rec["written_path"] = path
                seen[sha] = path.name
            rec["status"] = "new"
            rec["dup_of"] = None
            rows.append(rec)
            written += 1
            if sheet == MASTER:
                pending.append((rec, blob))
        if args.limit and written >= args.limit:
            break

    # The first pass saved 13 large PNGs as re-encoded JPEG, so their byte hashes
    # match nothing. Compare a coarse thumbnail against the files no byte-hash
    # claimed, and treat a match as "already extracted".
    leftovers = {h: n for h, n in disk_reg.items() if h not in used_disk}
    if leftovers:
        print(
            f"\n{len(leftovers)} on-disk file(s) matched no workbook image by bytes; "
            f"checking {len(pending)} consolidated-tab image(s) pixel-wise"
        )
        left_fp = {sha: _fingerprint((EXISTING / fname).read_bytes()) for sha, fname in leftovers.items()}
        for rec, blob in pending:
            fp = _fingerprint(blob)
            hit = next((sha for sha, other in left_fp.items() if _same_picture(fp, other)), None)
            if hit is None:
                continue
            written_path = rec.pop("written_path", None)
            rec["filename"] = leftovers[hit]
            rec["ext"] = Path(rec["filename"]).suffix.lstrip(".")
            rec["status"] = "existing_reencoded"
            written -= 1
            left_fp.pop(hit, None)
            if written_path is not None:
                written_path.unlink(missing_ok=True)

    df = pd.DataFrame(rows)
    if df.empty:
        raise SystemExit("no embedded images found")

    counts = df.groupby(["sheet", "status"]).size().unstack(fill_value=0)
    print()
    print(counts.to_string())
    n_dup = int((df["status"] == "duplicate").sum())
    n_new = int((df["status"] == "new").sum())
    n_re = int((df["status"] == "existing_reencoded").sum())
    print()
    print(f"embedded images:      {len(df)}")
    print(f"unique pictures:      {len(df) - n_dup}")
    print(f"already extracted:    {len(df) - n_dup - n_new}  (of which re-encoded: {n_re})")
    print(f"newly exported:       {n_new}  -> {outdir}")
    print(f"duplicate snapshots:  {n_dup}")

    if args.dry_run:
        print("\ndry run - nothing written")
        return

    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    cols = ["sheet", "slug", "row", "col", "name", "sha1", "ext", "filename", "status", "dup_of"]
    df.reindex(columns=cols).to_csv(MANIFEST, index=False, encoding="utf-8-sig")
    print(f"wrote {MANIFEST}")


if __name__ == "__main__":
    main()
