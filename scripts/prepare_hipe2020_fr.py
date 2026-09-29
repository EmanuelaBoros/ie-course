#!/usr/bin/env python3
"""Reproduce the four-column HIPE-2022 v2.1 French teaching dataset."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

COMMIT = "147f5bc3c7fb7e5c6b024a9ffd6503cd019fb9ea"
SOURCE_PATH = "data/v2.1/hipe2020/fr"
BASE = f"https://raw.githubusercontent.com/hipe-eval/HIPE-2022-data/{COMMIT}"
COLUMNS = ["TOKEN", "NE-COARSE-LIT", "NEL-LIT", "MISC"]
SPLITS = ["train", "dev", "test", "test_ELmasked", "test_allmasked"]


def project(raw):
    """Select columns by header; retain comments and blank lines verbatim."""
    lines = raw.decode("utf-8-sig").splitlines(keepends=True)
    header = lines[0].rstrip("\r\n").split("\t")
    indices = [header.index(column) for column in COLUMNS]
    output = ["\t".join(COLUMNS) + "\n"]
    tokens = documents = sentence_markers = 0
    for number, line in enumerate(lines[1:], 2):
        stripped = line.rstrip("\r\n")
        if not stripped or stripped.startswith("# "):
            output.append(line)
            documents += stripped.startswith("# hipe2022:document_id = ")
            continue
        fields = stripped.split("\t")
        if len(fields) != len(header):
            raise ValueError(f"Line {number}: expected {len(header)} fields, got {len(fields)}")
        ending = line[len(stripped):]
        output.append("\t".join(fields[i] for i in indices) + ending)
        tokens += 1
        sentence_markers += "EndOfSentence" in fields[header.index("MISC")].split("|")
    return "".join(output).encode("utf-8"), {
        "documents": documents, "tokens": tokens,
        "end_of_sentence_markers": sentence_markers,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, help="Optional local upstream French TSV folder")
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parents[1] / "data/hipe2020-fr")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"source_repository": "https://github.com/hipe-eval/HIPE-2022-data",
                "source_commit": COMMIT, "source_path": SOURCE_PATH,
                "columns": COLUMNS, "license": "CC-BY-NC-SA-4.0", "files": []}
    for split in SPLITS:
        name = f"HIPE-2022-v2.1-hipe2020-{split}-fr.tsv"
        url = f"{BASE}/{SOURCE_PATH}/{name}"
        if args.source_dir:
            raw = (args.source_dir / name).read_bytes()
        else:
            with urlopen(url, timeout=60) as response:
                raw = response.read()
        reduced, counts = project(raw)
        (args.output_dir / name).write_bytes(reduced)
        manifest["files"].append({"file": name, "split": split, "source_url": url,
                                  "source_sha256": hashlib.sha256(raw).hexdigest(),
                                  "sha256": hashlib.sha256(reduced).hexdigest(), **counts})
        print(f"{split}: {counts['documents']} documents; {counts['tokens']} tokens")
    (args.output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
