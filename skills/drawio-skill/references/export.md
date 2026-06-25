# Draw.io Export

Use this reference when exporting `.drawio` files through the draw.io desktop CLI.

## Preview Export

Preview PNGs are for visual inspection. Do not embed diagram XML in preview PNGs.

```bash
drawio -x -f png --width 2000 -o diagram.png input.drawio
```

Use `--width` rather than `-w`. Do not combine `--width` with `-s`.

## Final Editable PNG

Use `-e` for final PNGs so the PNG contains editable diagram XML. Use a `.drawio.png` double extension.

```bash
drawio -x -f png -e -s 2 -o diagram.drawio.png input.drawio
python3 <this-skill-dir>/scripts/repair_png.py diagram.drawio.png
```

Run `repair_png.py` immediately after every `-e` PNG export. The script is safe to run even if draw.io later fixes the truncated `IEND` issue.

## Other Formats

```bash
drawio -x -f svg -e -o diagram.svg input.drawio
drawio -x -f pdf -e -o diagram.pdf input.drawio
drawio -x -f jpg -o diagram.jpg input.drawio
```

## Useful Flags

- `-x`: export mode.
- `-f`: output format, such as `png`, `svg`, `pdf`, or `jpg`.
- `-e`: embed diagram XML in PNG/SVG/PDF.
- `-s`: scale, usually `2` for final PNG.
- `--width`: target width for preview images.
- `-o`: output path.
- `-b`: border width.
- `-t`: transparent PNG background.
- `--page-index N`: export one page.

## Fallbacks

- If CLI is missing but Python works, use `scripts/encode_drawio_url.py` to generate a diagrams.net URL.
- If CLI is missing and Python is missing, deliver the `.drawio` XML and ask the user to open it manually.
- If Linux export fails, retry with `xvfb-run -a`; on root CI, append `--no-sandbox` at the end.
- If macOS sandbox isolation crashes the app, treat CLI export as unavailable in that sandbox and use the browser fallback.
