#!/usr/bin/env python3
"""Demo: turn the Pixel Lab LLM doc into a lightweight Python client.

Run from repo root:
    python examples/pixellab_module_demo.py \
        --output examples/generated/pixellab_client.py

What it does:
- Downloads the LLM-friendly docs at https://api.pixellab.ai/v2/llms.txt (or reads a local file)
- Parses the endpoints (method, path, title/tag)
- Generates a minimal `PixelLabClient` with one method per endpoint
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import requests

PIXELLAB_LLM_URL = "https://api.pixellab.ai/v2/llms.txt"
DEFAULT_BASE_URL = "https://api.pixellab.ai/v2"


@dataclass(frozen=True)
class Endpoint:
    method: str
    path: str
    title: Optional[str] = None
    tag: Optional[str] = None


def fetch_doc(source: str) -> str:
    """Fetch documentation from a URL or local file."""
    if source.startswith(("http://", "https://")):
        resp = requests.get(source, timeout=30)
        resp.raise_for_status()
        return resp.text
    return Path(source).read_text(encoding="utf-8")


def parse_endpoints(doc_text: str) -> List[Endpoint]:
    """Extract endpoints from the LLM-friendly Markdown."""
    endpoints: List[Endpoint] = []
    lines = doc_text.splitlines()
    pattern = re.compile(r"^##\s+(GET|POST)\s+(/[\w\-/{}]+)")

    for idx, raw in enumerate(lines):
        line = raw.strip()
        match = pattern.match(line)
        if not match:
            continue

        method, path = match.groups()
        title, tag = None, None

        # Look ahead for bold title and tag lines
        cursor = idx + 1
        while cursor < len(lines) and not lines[cursor].strip():
            cursor += 1
        if cursor < len(lines):
            candidate = lines[cursor].strip()
            if candidate.startswith("**") and candidate.endswith("**"):
                title = candidate.strip("* ").strip()
                cursor += 1

        while cursor < len(lines) and not lines[cursor].strip():
            cursor += 1
        if cursor < len(lines):
            candidate = lines[cursor].strip()
            if candidate.lower().startswith("tags:"):
                tag = candidate.split(":", 1)[1].strip()

        endpoints.append(Endpoint(method=method, path=path, title=title, tag=tag))

    return endpoints


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    if not slug:
        slug = "endpoint"
    if slug[0].isdigit():
        slug = f"fn_{slug}"
    return slug


def unique_names(endpoints: Iterable[Endpoint]) -> Dict[Endpoint, str]:
    """Assign deterministic, unique function names."""
    seen: Dict[str, int] = {}
    mapping: Dict[Endpoint, str] = {}
    for ep in endpoints:
        base = slugify(ep.title or f"{ep.method} {ep.path}")
        count = seen.get(base, 0)
        seen[base] = count + 1
        name = f"{base}_{count+1}" if count else base
        mapping[ep] = name
    return mapping


def render_client(endpoints: List[Endpoint], base_url: str, source: str) -> str:
    """Render the Python client module as a string."""
    name_map = unique_names(endpoints)
    lines: List[str] = []

    lines.append('"""Auto-generated Pixel Lab API client.')
    lines.append("")
    lines.append(f"Generated from: {source}")
    lines.append('This file is produced by examples/pixellab_module_demo.py')
    lines.append('"""')
    lines.append("")
    lines.append("from typing import Any, Dict, Optional")
    lines.append("")
    lines.append("import requests")
    lines.append("")
    lines.append("")
    lines.append("class PixelLabClient:")
    lines.append(
        f"    def __init__(self, api_token: str, base_url: str = \"{base_url}\", timeout: int = 30):"
    )
    lines.append("        self.api_token = api_token")
    lines.append("        self.base_url = base_url.rstrip('/')")
    lines.append("        self.timeout = timeout")
    lines.append("")
    lines.append("    def _request(")
    lines.append("        self,")
    lines.append("        method: str,")
    lines.append("        path: str,")
    lines.append("        params: Optional[Dict[str, Any]] = None,")
    lines.append("        payload: Optional[Dict[str, Any]] = None,")
    lines.append("    ) -> Dict[str, Any]:")
    lines.append('        """Internal request helper."""')
    lines.append("        url = f\"{self.base_url}{path}\"")
    lines.append("        headers = {")
    lines.append('            "Authorization": f"Bearer {self.api_token}",')
    lines.append('            "Content-Type": "application/json",')
    lines.append("        }")
    lines.append(
        "        response = requests.request("
        "method=method, url=url, headers=headers, params=params, json=payload, timeout=self.timeout"
        ")"
    )
    lines.append("        response.raise_for_status()")
    lines.append("        return response.json()")
    lines.append("")

    for ep in endpoints:
        func_name = name_map[ep]
        path_params = re.findall(r"{([^}]+)}", ep.path)
        param_sig = [f"{p}: str" for p in path_params]
        if ep.method == "GET":
            param_sig.append("params: Optional[Dict[str, Any]] = None")
        else:
            param_sig.append("payload: Optional[Dict[str, Any]] = None")
        sig = ", ".join(["self"] + param_sig)

        lines.append(f"    def {func_name}({sig}) -> Dict[str, Any]:")
        title = ep.title or ""
        doc = title if title else f"{ep.method} {ep.path}"
        if ep.tag:
            doc += f" | Tag: {ep.tag}"
        lines.append(f'        """{doc} ({ep.method} {ep.path})"""')
        if path_params:
            fstring_path = ep.path
            for p in path_params:
                fstring_path = fstring_path.replace("{" + p + "}", "{" + p + "}")
            lines.append(f"        path = f\"{fstring_path}\"")
        else:
            lines.append(f"        path = \"{ep.path}\"")

        if ep.method == "GET":
            lines.append("        return self._request(\"GET\", path, params=params)")
        else:
            lines.append("        return self._request(\"POST\", path, payload=payload)")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Pixel Lab client module from LLM docs.")
    parser.add_argument("--source", default=PIXELLAB_LLM_URL, help="URL or path to llms.txt (default: live URL)")
    parser.add_argument("--output", default="examples/generated/pixellab_client.py", help="Where to write the client module")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Base API URL to bake into the client")
    args = parser.parse_args()

    doc_text = fetch_doc(args.source)
    endpoints = parse_endpoints(doc_text)
    if not endpoints:
        raise SystemExit("No endpoints found in documentation.")

    code = render_client(endpoints, base_url=args.base_url, source=args.source)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(code, encoding="utf-8")

    print(f"Generated {len(endpoints)} endpoint methods -> {out_path}")
    sample = name_map_sample(endpoints)
    if sample:
        print("Sample call:")
        print(f"  from {out_path.stem} import PixelLabClient")
        print("  client = PixelLabClient(api_token='YOUR_TOKEN')")
        print(f"  client.{sample}(...)")


def name_map_sample(endpoints: List[Endpoint]) -> Optional[str]:
    """Pick a representative method name for the preview."""
    if not endpoints:
        return None
    return unique_names(endpoints)[endpoints[0]]


if __name__ == "__main__":
    main()
