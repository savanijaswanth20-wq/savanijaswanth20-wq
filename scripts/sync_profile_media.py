"""Cache verified profile media in the repository; existing valid files need no network."""
import hashlib
import json
from pathlib import Path
import re
import tempfile
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_PATHS = {
    "assets/hero.gif", "assets/hero-mobile.gif",
    "assets/hero.png", "assets/hero-mobile.png",
}
MEDIA_HOST = "d2ol7oe51mr4n9.cloudfront.net"
MAX_BYTES = 8 * 1024 * 1024


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    manifest = json.loads((ROOT / "assets/media-manifest.json").read_text())
    files = manifest["files"]
    if manifest.get("schema_version") != 1:
        raise ValueError("Unsupported media manifest")
    if len(files) != len(ALLOWED_PATHS) or {f["path"] for f in files} != ALLOWED_PATHS:
        raise ValueError("Manifest must contain exactly the four profile media files")
    for item in files:
        target = ROOT / item["path"]
        expected = item["sha256"]
        if not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise ValueError("Invalid SHA-256 checksum")
        source = urlparse(item["url"])
        if source.scheme != "https" or source.netloc != MEDIA_HOST:
            raise ValueError("Unexpected media source")
        if target.exists() and digest(target.read_bytes()) == expected:
            print(f"Verified cached {item['path']}")
            continue
        request = Request(item["url"], headers={"User-Agent": "Jaswanth-Profile-Assets/1.0"})
        with urlopen(request, timeout=60) as response:
            resolved = urlparse(response.geturl())
            if resolved.scheme != "https" or resolved.netloc != MEDIA_HOST:
                raise ValueError("Unexpected media redirect")
            data = response.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise ValueError("Media exceeds the 8 MiB limit")
        if digest(data) != expected:
            raise ValueError(f"Checksum mismatch for {item['path']}")
        if target.suffix == ".gif" and data[:6] not in (b"GIF87a", b"GIF89a"):
            raise ValueError("Expected GIF data")
        if target.suffix == ".png" and data[:8] != b"\x89PNG\r\n\x1a\n":
            raise ValueError("Expected PNG data")
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as temporary:
            temporary.write(data)
            staging = Path(temporary.name)
        try:
            staging.replace(target)
        finally:
            staging.unlink(missing_ok=True)
        print(f"Saved {item['path']} ({len(data):,} bytes)")


if __name__ == "__main__":
    main()
