#!/usr/bin/env python3
"""Check an OpenCode config for free-only model usage.

Usage:
    python check-free-models.py [path-to-config]
    python check-free-models.py --catalog

If no path is given, the script looks for opencode.json(c) or
.opencode/opencode.json(c) in the current directory.

`--catalog` fetches the live free-model list from models.dev instead of
checking a config. It needs network access.

Exit codes:
    0  all models are free
    1  at least one non-free model was found
    2  config not found, could not be parsed, or the catalog fetch failed
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Known free model IDs served through the opencode provider.
# Source: https://models.dev/api.json (provider "opencode", cost 0).
# Free offers rotate: any opencode model ending in "-free" is also accepted.
FREE_MODELS = {
    "beam-free",
    "big-pickle",
    "cat-jam-free",
    "crouton-alpha-free",
    "deepseek-v4-flash-free",
    "deepseek-v4.1-flash-free",
    "exo-free",
    "fledge-alpha-free",
    "flint-40b-free",
    "glm-4.7-free",
    "glm-5-free",
    "glm-5.3-flash-free",
    "grok-code",
    "hy3-free",
    "hy3-preview-free",
    "iceman-free",
    "inkling-2-small-free",
    "kimi-k2.5-free",
    "laguna-s-2.1-free",
    "ling-2.6-flash-free",
    "ling-3.0-flash-fin-free",
    "ling-3.0-flash-free",
    "ling-3.0-tiny-free",
    "ling-3.1-flash-free",
    "ll-alpha-free",
    "longcat-2.0-free",
    "longcat-2.5-free",
    "longcat-2.5-preview-free",
    "mimo-v2-flash-free",
    "mimo-v2-omni-free",
    "mimo-v2-pro-free",
    "mimo-v2.5-free",
    "mimo-v2.6-flash-free",
    "minimax-m2.1-free",
    "minimax-m2.5-free",
    "minimax-m3-free",
    "minimax-m3.1-flash-free",
    "muse-spark-1.2-contributor-free",
    "muse-spark-1.3-contributor-free",
    "nemotron-3-super-free",
    "nemotron-3-ultra-free",
    "nemotron-3.5-lightning-free",
    "nemotron-3.5-super-vl-free",
    "north-mini-code-free",
    "pulse-alpha-free",
    "qwen3.6-plus-free",
    "ring-2.6-1t-free",
    "space-bunny-free",
    "step-5-preview-free",
    "trinity-large-preview-free",
    "x-preview-f-free",
}


def strip_jsonc(text: str) -> str:
    """Remove block comments, line comments, and trailing commas."""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)

    lines: list[str] = []
    for line in text.splitlines():
        in_string = False
        escape = False
        cut = None
        for i, ch in enumerate(line):
            if escape:
                escape = False
                continue
            if ch == "\\":
                escape = True
                continue
            if ch == '"':
                in_string = not in_string
                continue
            if not in_string and ch == "/" and i + 1 < len(line) and line[i + 1] == "/":
                cut = i
                break
        lines.append(line[:cut] if cut is not None else line)

    text = "\n".join(lines)
    text = re.sub(r",(\s*[}\]])", r"\1", text)
    return text


def find_config(explicit: str | None) -> Path | None:
    if explicit:
        path = Path(explicit)
        return path if path.exists() else None
    for candidate in (
        "opencode.jsonc",
        "opencode.json",
        ".opencode/opencode.jsonc",
        ".opencode/opencode.json",
    ):
        path = Path(candidate)
        if path.exists():
            return path
    return None


def model_is_free(provider: str, model: str) -> bool:
    if provider != "opencode":
        return False
    if model in FREE_MODELS:
        return True
    return model.endswith("-free")


def print_catalog() -> int:
    """Fetch the live free-model list from models.dev."""
    import urllib.request

    url = "https://models.dev/api.json"
    print(f"Fetching {url}", flush=True)
    try:
        request = urllib.request.Request(
            url, headers={"User-Agent": "free-orchestrate/1.0"}
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            catalog = json.loads(response.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(f"Could not fetch the catalog: {exc}", file=sys.stderr)
        return 2

    models = (catalog.get("opencode") or {}).get("models") or {}
    rows = []
    for model_id, model in models.items():
        cost = model.get("cost") or {}
        if cost.get("input") or cost.get("output"):
            continue
        limit = model.get("limit") or {}
        rows.append(
            (
                model_id,
                model.get("name", ""),
                limit.get("context", 0),
                limit.get("output", 0),
            )
        )

    rows.sort(key=lambda row: -int(row[2] or 0))
    print(f"\n{len(rows)} free models on the opencode provider:\n")
    print(f"{'ID':<38} {'CONTEXT':>9} {'OUTPUT':>9}  NAME")
    for model_id, name, context, output in rows:
        print(f"{model_id:<38} {context:>9,} {output:>9,}  {name}")
    print("\nCopy the IDs you need into your config, then run this script on it.")
    return 0


def main() -> int:
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg in ("--catalog", "-c", "--list-catalog"):
        return print_catalog()

    path = find_config(arg)
    if path is None:
        print("No OpenCode config found.", file=sys.stderr)
        return 2

    print(f"Checking {path}")
    try:
        data = json.loads(strip_jsonc(path.read_text(encoding="utf-8-sig")))
    except Exception as exc:  # noqa: BLE001
        print(f"Failed to parse {path}: {exc}", file=sys.stderr)
        return 2

    selectors: list[tuple[str, object]] = []
    if data.get("model"):
        selectors.append(("root model", data["model"]))
    for name, agent in (data.get("agents") or {}).items():
        if isinstance(agent, dict) and agent.get("model"):
            selectors.append((f"agent:{name}", agent["model"]))

    problems = 0
    for label, selector in selectors:
        if isinstance(selector, dict):
            provider = selector.get("providerID", "")
            model = selector.get("model", "")
        else:
            parts = str(selector).split("/", 1)
            provider = parts[0]
            model = parts[1] if len(parts) > 1 else ""

        if model_is_free(provider, model):
            print(f"  free      {label}: {selector}")
        else:
            print(f"  NON-FREE  {label}: {selector}")
            problems += 1

    if problems:
        print(f"\n{problems} non-free model(s) found. Use only free OpenCode models.")
        return 1

    print("\nAll models are free.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
