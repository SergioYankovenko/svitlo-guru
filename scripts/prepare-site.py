"""Publish the existing static release on an additional domain."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import urllib.error
import urllib.request


def main():
    upstream, destination = map(Path, sys.argv[1:3])
    source_sha = subprocess.check_output(
        ["git", "-C", str(upstream), "rev-parse", "HEAD"], text=True
    ).strip()
    version = {
        "source_repository": "SergioYankovenko/svitlo",
        "source_sha": source_sha,
        "publisher_sha": os.environ.get("GITHUB_SHA", "local"),
    }
    changed = True
    if os.environ.get("GITHUB_EVENT_NAME") == "schedule":
        request = urllib.request.Request(
            "https://svitlo.guru/deployment-source.json",
            headers={"Cache-Control": "no-cache"},
        )
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                changed = json.load(response) != version
        except (OSError, ValueError, urllib.error.URLError):
            # DNS propagation or the first deployment can make the site unavailable.
            pass

    if changed:
        destination.mkdir(parents=True, exist_ok=True)
        names = ["index.html", "assets", "app", "downloads", "update.json"]
        names.extend(
            name for name in ("license.html", "LICENSE", "NOTICE", "LICENSING.md", "LICENSES")
            if (upstream / name).exists()
        )
        for name in names:
            source = upstream / name
            if source.is_dir():
                shutil.copytree(source, destination / name, dirs_exist_ok=True)
            else:
                shutil.copy2(source, destination / name)
        (destination / ".nojekyll").touch()
        (destination / "CNAME").write_text("svitlo.guru\n", encoding="utf-8")
        for name in ("index.html", "license.html"):
            page = destination / name
            if page.exists():
                page.write_text(
                    page.read_text(encoding="utf-8").replace(
                        "https://sergioyankovenko.github.io/svitlo/", "https://svitlo.guru/"
                    ),
                    encoding="utf-8",
                )
        (destination / "deployment-source.json").write_text(
            json.dumps(version, indent=2) + "\n", encoding="utf-8"
        )
    if output := os.environ.get("GITHUB_OUTPUT"):
        with open(output, "a", encoding="utf-8") as stream:
            stream.write(f"changed={str(changed).lower()}\n")
    print(json.dumps({"changed": changed, **version}))


if __name__ == "__main__":
    main()
