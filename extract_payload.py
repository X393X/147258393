#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import io
import zipfile
from pathlib import Path

EXPECTED_SHA256 = "038c9e6d426862550972e614dcf7a6c34e3f9e2bd341df440362c64df701ea1f"


def main() -> None:
    root = Path(__file__).resolve().parent
    chunks = sorted((root / "payload").glob("payload-*.txt"))
    if not chunks:
        raise SystemExit("No payload chunks found")
    encoded = "".join(path.read_text().strip() for path in chunks)
    data = base64.b64decode(encoded)
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"Payload SHA-256 mismatch: {digest}")
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        archive.testzip()
        archive.extractall(root)
        print(f"Extracted {len(archive.namelist())} Todaysunny source files")


if __name__ == "__main__":
    main()
