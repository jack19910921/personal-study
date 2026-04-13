#!/usr/bin/env python3
"""Create a local workspace for an arXiv paper and download its assets."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import error, parse, request
from xml.etree import ElementTree

DEFAULT_BASE_DIR = Path("~/personal-study/papers").expanduser()
USER_AGENT = "paper-reading/1.0 (+https://arxiv.org)"
ATOM_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a local arXiv paper workspace and download PDF/source."
    )
    parser.add_argument("url", help="arXiv URL, such as https://arxiv.org/abs/2401.00001")
    parser.add_argument(
        "base_dir",
        nargs="?",
        default=str(DEFAULT_BASE_DIR),
        help="Base directory for paper folders. Defaults to ~/personal-study/papers",
    )
    return parser.parse_args()


def extract_arxiv_id(url: str) -> str:
    parsed = parse.urlparse(url)
    if "arxiv.org" not in parsed.netloc:
        raise ValueError(f"Unsupported domain: {parsed.netloc or url}")

    path = parsed.path.strip("/")
    if not path:
        raise ValueError(f"Could not extract arXiv ID from URL: {url}")

    if path.startswith(("abs/", "pdf/", "html/", "e-print/")):
        paper_id = path.split("/", 1)[1]
    else:
        paper_id = path

    if paper_id.endswith(".pdf"):
        paper_id = paper_id[:-4]

    paper_id = paper_id.strip()
    if not paper_id:
        raise ValueError(f"Could not extract arXiv ID from URL: {url}")
    return paper_id


def http_get(url: str) -> request.addinfourl:
    req = request.Request(url, headers={"User-Agent": USER_AGENT})
    return request.urlopen(req, timeout=30)


def fetch_metadata(arxiv_id: str) -> dict[str, Any]:
    encoded_id = parse.quote(arxiv_id, safe="")
    api_url = f"https://export.arxiv.org/api/query?id_list={encoded_id}"
    with http_get(api_url) as response:
        xml_bytes = response.read()

    root = ElementTree.fromstring(xml_bytes)
    entry = root.find("atom:entry", ATOM_NS)
    if entry is None:
        raise RuntimeError(f"No metadata returned for arXiv ID: {arxiv_id}")

    def text(path: str) -> str:
        node = entry.find(path, ATOM_NS)
        if node is None or node.text is None:
            return ""
        return " ".join(node.text.split())

    authors = [
        " ".join(author.text.split())
        for author in entry.findall("atom:author/atom:name", ATOM_NS)
        if author.text
    ]
    categories = [
        cat.attrib["term"]
        for cat in entry.findall("atom:category", ATOM_NS)
        if cat.attrib.get("term")
    ]

    primary_category_node = entry.find("arxiv:primary_category", ATOM_NS)
    primary_category = (
        primary_category_node.attrib.get("term", "") if primary_category_node is not None else ""
    )

    return {
        "arxiv_id": arxiv_id,
        "title": text("atom:title"),
        "abstract": text("atom:summary"),
        "authors": authors,
        "published": text("atom:published"),
        "updated": text("atom:updated"),
        "comment": text("arxiv:comment"),
        "journal_ref": text("arxiv:journal_ref"),
        "doi": text("arxiv:doi"),
        "primary_category": primary_category,
        "categories": categories,
        "abs_url": f"https://arxiv.org/abs/{arxiv_id}",
        "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
        "source_url": f"https://arxiv.org/e-print/{arxiv_id}",
    }


def sanitize_folder_name(title: str, fallback: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|]+', " ", title)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")
    if not cleaned:
        cleaned = fallback.replace("/", "-")
    return cleaned[:120].rstrip(" .")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def download_to_path(url: str, destination: Path) -> Path:
    with http_get(url) as response, destination.open("wb") as fh:
        while True:
            chunk = response.read(1024 * 64)
            if not chunk:
                break
            fh.write(chunk)
    return destination


def infer_source_filename(headers: Any) -> str:
    content_disposition = headers.get("Content-Disposition", "")
    match = re.search(r'filename="?([^";]+)"?', content_disposition)
    if match:
        return match.group(1)

    content_type = headers.get_content_type()
    if "gzip" in content_type:
        return "source.tar.gz"
    if "tar" in content_type:
        return "source.tar"
    if content_type == "application/pdf":
        return "source.pdf"
    return "source"


def download_source(url: str, paper_dir: Path) -> Path | None:
    try:
        with http_get(url) as response:
            filename = infer_source_filename(response.headers)
            destination = paper_dir / filename
            with destination.open("wb") as fh:
                while True:
                    chunk = response.read(1024 * 64)
                    if not chunk:
                        break
                    fh.write(chunk)
            return destination
    except error.HTTPError as exc:
        if exc.code in {403, 404}:
            return None
        raise


def maybe_extract_source(source_path: Path | None, paper_dir: Path) -> Path | None:
    if source_path is None or not source_path.exists():
        return None

    extract_dir = paper_dir / "source"
    ensure_dir(extract_dir)
    try:
        with tarfile.open(source_path, "r:*") as archive:
            base = extract_dir.resolve()
            for member in archive.getmembers():
                target = (extract_dir / member.name).resolve()
                if not str(target).startswith(str(base) + "/") and target != base:
                    raise RuntimeError(f"Unsafe archive member path: {member.name}")
            archive.extractall(extract_dir)
        return extract_dir
    except (tarfile.TarError, RuntimeError):
        return None


def write_metadata(metadata: dict[str, Any], metadata_path: Path) -> None:
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def make_slug(title: str) -> str:
    """Create a URL-safe slug from the title for file naming."""
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")[:80]


def make_date_slug(metadata: dict[str, Any]) -> str:
    """Create a date slug from published date, e.g. 2024-04."""
    published = metadata.get("published", "")
    if published:
        return published[:7].replace("-", "-")
    return "unknown"


def maybe_create_report(report_path: Path, metadata: dict[str, Any]) -> None:
    if report_path.exists():
        return

    authors = "、".join(metadata["authors"]) if metadata["authors"] else "未知"
    categories = ", ".join(metadata["categories"]) if metadata["categories"] else "未知"
    created_at = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    date_slug = make_date_slug(metadata)
    title_slug = make_slug(metadata["title"])
    reading_date = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d")

    report = f"""# Paper Reading: {metadata['title']}

> **Authors**: {authors}
> **arXiv ID**: {metadata['arxiv_id']}
> **Source**: {metadata['abs_url']}
> **Published**: {metadata['published'] or '未知'}
> **学科分类**: {categories}
> **Reading Date**: {reading_date}
> **本地文件**:
> - PDF: `pdf/`
> - Source: `source/` (如可用)

## 一句话总结

待补充。

## 论文要解决什么问题

- 研究背景
- 现有方法的短板
- 论文的切入点

## 核心思路

用自然语言先解释，再拆成 3-6 个关键模块。

```mermaid
flowchart TD
    A[研究问题] --> B[核心方法]
    B --> C[实验验证]
    C --> D[结论]
```

## 方法细拆

### 1. 模块 A

- 输入是什么
- 做了什么变换
- 输出到哪里
- 为什么这样设计

### 2. 模块 B

同上。

## 训练 / 推理流程

如果论文更偏训练，就重点解释训练；如果更偏系统或推理，就重点解释推理链路。

```mermaid
sequenceDiagram
    participant U as 输入
    participant M1 as 模块1
    participant M2 as 模块2
    participant O as 输出
    U->>M1: 数据/指令
    M1->>M2: 中间表示
    M2->>O: 结果
```

## 实验设置与结果

- 数据集
- Baseline
- 指标
- 主结果
- 消融实验
- 失败案例或负面结果

建议把"论文声称什么"与"你如何理解这些结果"分开写。

## 这篇论文真正的贡献

- 贡献 1
- 贡献 2
- 贡献 3

## 局限与适用边界

- 论文自己承认的局限
- 从实验设计能看出的边界
- 真实落地时可能遇到的问题

## 对后续研究/应用的启发

- 值得复现的部分
- 值得继续验证的假设
- 对工程应用的意义

## 术语表

待补充。

## 原始摘要

{metadata['abstract'] or '无'}

## 复查记录

- {created_at}: 初始化论文目录并创建报告骨架。
"""
    report_path.write_text(report, encoding="utf-8")


def main() -> int:
    args = parse_args()
    base_dir = Path(args.base_dir).expanduser().resolve()
    ensure_dir(base_dir)

    arxiv_id = extract_arxiv_id(args.url)
    metadata = fetch_metadata(arxiv_id)

    # Create dated directory: papers/2024-04-paper-title/
    date_slug = make_date_slug(metadata)
    title_slug = make_slug(metadata["title"])
    folder_name = f"{date_slug}-{title_slug}"
    if not folder_name:
        folder_name = arxiv_id

    paper_dir = base_dir / folder_name
    ensure_dir(paper_dir)

    pdf_filename = sanitize_folder_name(metadata["title"], arxiv_id) + ".pdf"
    pdf_path = download_to_path(metadata["pdf_url"], paper_dir / pdf_filename)
    source_path = download_source(metadata["source_url"], paper_dir)
    source_extract_dir = maybe_extract_source(source_path, paper_dir)
    report_filename = sanitize_folder_name(metadata["title"], arxiv_id) + "_报告.md"
    report_path = paper_dir / report_filename

    metadata["paper_dir"] = str(paper_dir)
    metadata["pdf_path"] = str(pdf_path)
    metadata["source_path"] = str(source_path) if source_path else None
    metadata["source_extract_dir"] = str(source_extract_dir) if source_extract_dir else None
    metadata["report_path"] = str(report_path)
    metadata["downloaded_at"] = datetime.now(timezone.utc).isoformat()

    write_metadata(metadata, paper_dir / "metadata.json")
    maybe_create_report(report_path, metadata)

    print(
        json.dumps(
            {
                "paper_dir": str(paper_dir),
                "report_path": str(report_path),
                "pdf_path": str(pdf_path),
                "source_path": str(source_path) if source_path else None,
                "source_extract_dir": str(source_extract_dir) if source_extract_dir else None,
                "metadata_path": str(paper_dir / "metadata.json"),
                "arxiv_id": arxiv_id,
                "title": metadata["title"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        sys.exit(130)
