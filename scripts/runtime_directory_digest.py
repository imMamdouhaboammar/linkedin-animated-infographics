import hashlib
import os
from pathlib import Path


def directory_descriptor(path):
    digest = hashlib.sha256()
    files = 0
    total = 0
    for root, directories, filenames in os.walk(path, followlinks=False):
        directories.sort()
        filenames.sort()
        for directory in directories:
            current = Path(root) / directory
            if current.is_symlink():
                relative = current.relative_to(path).as_posix()
                raise ValueError(f"directory artifact contains symlink: {relative}")
        for filename in filenames:
            current = Path(root) / filename
            relative = current.relative_to(path).as_posix().encode()
            if current.is_symlink():
                raise ValueError(f"directory artifact contains symlink: {relative.decode()}")
            size = current.stat().st_size
            digest.update(len(relative).to_bytes(8, "big"))
            digest.update(relative)
            digest.update(size.to_bytes(8, "big"))
            with current.open("rb") as stream:
                for chunk in iter(lambda: stream.read(65536), b""):
                    digest.update(chunk)
            files += 1
            total += size
    return {"$directory_sha256": digest.hexdigest(), "$files": files, "$size": total}
