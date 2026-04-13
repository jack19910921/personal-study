#!/usr/bin/env python3
"""
Source Code Reading - 仓库分析和初始化脚本

功能：
1. 解析 GitHub URL
2. 检查仓库是否已在本地
3. 如果不在，提示克隆
4. 创建分析目录
5. 生成仓库结构信息
"""

import os
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime


def parse_github_url(url):
    """解析 GitHub URL，提取 owner 和 repo"""
    patterns = [
        r'github\.com/([^/]+)/([^/]+?)(\.git)?/?$',
        r'github\.com/([^/]+)/([^/]+?)$',
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            groups = match.groups()
            owner = groups[0]
            repo = groups[1].replace('.git', '') if len(groups) > 1 else ''
            return owner, repo

    raise ValueError(f"无法解析 GitHub URL: {url}")


def check_repo_exists(github_dir, owner, repo):
    """检查仓库是否已在本地"""
    repo_path = Path(github_dir) / repo
    if repo_path.exists():
        git_dir = repo_path / '.git'
        if git_dir.exists():
            return True, str(repo_path)

    return False, None


def get_repo_info(repo_path):
    """获取仓库基本信息"""
    info = {
        'name': Path(repo_path).name,
        'path': str(repo_path),
        'last_commit': None,
        'branch': None,
    }

    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            info['branch'] = result.stdout.strip()

        result = subprocess.run(
            ['git', 'log', '-1', '--format=%ci'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            info['last_commit'] = result.stdout.strip()

    except Exception as e:
        info['error'] = str(e)

    return info


def generate_structure_file(repo_path, output_path, max_depth=3):
    """生成仓库结构文件"""
    try:
        exclude_dirs = {
            'node_modules', 'target', '__pycache__', 'dist', 'build',
            '.git', '.vscode', '.idea', 'vendor', 'venv', 'env',
        }

        result = subprocess.run(
            ['tree', '-L', str(max_depth), '-I', ','.join(exclude_dirs), '-a'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            output_path.write_text(result.stdout, encoding='utf-8')
            return True
        else:
            result = subprocess.run(
                ['find', '.', '-type', 'd', '-maxdepth', str(max_depth), '-not', '-path', '*/.*'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            output_path.write_text("# Directory Structure\n\n" + result.stdout, encoding='utf-8')
            return True

    except Exception as e:
        print(f"生成结构文件失败: {e}")
        return False


def count_lines_of_code(repo_path):
    """统计代码行数（简单统计）"""
    extensions = {
        '.ts': 'TypeScript',
        '.tsx': 'TypeScript',
        '.js': 'JavaScript',
        '.jsx': 'JavaScript',
        '.py': 'Python',
        '.go': 'Go',
        '.rs': 'Rust',
        '.java': 'Java',
        '.c': 'C',
        '.cpp': 'C++',
        '.h': 'C/C++ Header',
        '.cs': 'C#',
        '.rb': 'Ruby',
        '.php': 'PHP',
    }

    stats = {}

    try:
        for ext, lang in extensions.items():
            result = subprocess.run(
                ['find', '.', '-name', f'*{ext}', '-type', 'f'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                files = [f for f in result.stdout.strip().split('\n') if f]
                total_lines = 0

                for file in files:
                    try:
                        result = subprocess.run(
                            ['wc', '-l', file],
                            cwd=repo_path,
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        if result.returncode == 0:
                            total_lines += int(result.stdout.split()[0])
                    except Exception:
                        pass

                if total_lines > 0:
                    stats[lang] = {
                        'files': len(files),
                        'lines': total_lines
                    }
    except Exception as e:
        print(f"统计代码行数失败: {e}")

    return stats


def main():
    import sys

    if len(sys.argv) < 3:
        print("用法: python bootstrap_source_analysis.py <github_url> <base_dir>")
        print("示例: python bootstrap_source_analysis.py https://github.com/user/repo ~/personal-study/source-code")
        sys.exit(1)

    github_url = sys.argv[1]
    base_dir = sys.argv[2]

    try:
        owner, repo = parse_github_url(github_url)
        print(f"✓ 解析 GitHub 仓库: {owner}/{repo}")

        github_dir = os.path.expanduser('~/personal-study/coding/github')

        exists, repo_path = check_repo_exists(github_dir, owner, repo)

        if exists:
            print(f"✓ 仓库已在本地: {repo_path}")
        else:
            print(f"✗ 仓库不在本地")
            print(f"  请先克隆: git clone https://github.com/{owner}/{repo}.git")
            print(f"  目标目录: {github_dir}/{repo}")
            sys.exit(1)

        repo_info = get_repo_info(repo_path)
        print(f"✓ 当前分支: {repo_info.get('branch', 'unknown')}")

        analysis_dir = Path(base_dir).expanduser().resolve() / repo
        analysis_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ 创建分析目录: {analysis_dir}")

        structure_file = analysis_dir / 'structure.txt'
        if generate_structure_file(repo_path, structure_file):
            print(f"✓ 生成结构文件: {structure_file}")

        loc_stats = count_lines_of_code(repo_path)

        metadata = {
            'github_url': github_url,
            'owner': owner,
            'repo': repo,
            'repo_path': repo_path,
            'analysis_dir': str(analysis_dir),
            'branch': repo_info.get('branch'),
            'last_commit': repo_info.get('last_commit'),
            'analysis_date': datetime.now().isoformat(),
            'loc_stats': loc_stats
        }

        metadata_file = analysis_dir / 'metadata.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        print(f"✓ 生成元数据文件: {metadata_file}")
        print(f"\n分析目录已创建: {analysis_dir}")
        print(f"开始解读吧！")

        # 输出关键路径（供 AI 读取）
        print(f"\n# OUTPUT_START")
        print(f"repo_dir={repo_path}")
        print(f"analysis_dir={analysis_dir}")
        print(f"metadata_path={metadata_file}")
        print(f"structure_path={structure_file}")
        print(f"# OUTPUT_END")

    except ValueError as e:
        print(f"✗ 错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ 未知错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
