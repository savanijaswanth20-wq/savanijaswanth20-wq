#!/usr/bin/env python3
"""Refresh public GitHub metrics and README links using the repository owner.

Python standard library only. No personal access token or pip packages needed.
The workflow supplies its temporary GITHUB_TOKEN; do not paste a token here.
"""

import html
import json
import os
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.github.com"


def get_json(path):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "jaswanth-profile-updater",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    request = Request(API + path, headers=headers)
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def get_repositories(owner):
    repositories = []
    page = 1
    while True:
        batch = get_json(
            f"/users/{quote(owner, safe='')}/repos?type=owner&per_page=100&page={page}"
        )
        repositories.extend(batch)
        if len(batch) < 100:
            return repositories
        page += 1


def replace_section(text, name, content):
    start = f"<!-- {name}:START -->"
    end = f"<!-- {name}:END -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if len(pattern.findall(text)) != 1:
        raise ValueError(f"Expected exactly one {name} marker pair in README.md")
    return pattern.sub(lambda _: f"{start}\n{content}\n{end}", text)


def render_stats(owner, public_repos, followers, stars):
    title = html.escape(f"@{owner} / PUBLIC ACTIVITY")
    metrics = [
        (public_repos, "PUBLIC REPOSITORIES", "#69f0c2"),
        (followers, "FOLLOWERS", "#a69aff"),
        (stars, "STARS ON ORIGINAL REPOS", "#f0c987"),
    ]
    cards = []
    for i, (number, label, color) in enumerate(metrics):
        x = 24 + i * 316
        cards.append(f'''<g transform="translate({x},65)">
          <rect width="300" height="142" rx="16" fill="#11182a" stroke="#273148"/>
          <text x="22" y="68" fill="{color}" font-size="44" font-weight="700">{int(number):,}</text>
          <text x="22" y="107" fill="#b3bed1" font-size="12" letter-spacing="1">{label}</text>
          <path class="accent" d="M22 126 H278" stroke="{color}" stroke-width="2" pathLength="100"/>
        </g>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="980" height="236" viewBox="0 0 980 236" role="img" aria-labelledby="title desc">
      <title id="title">GitHub public statistics for {html.escape(owner)}</title>
      <desc id="desc">{public_repos} public repositories, {followers} followers, and {stars} stars on owned public non-fork repositories.</desc>
      <style>
        text {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; }}
        .accent {{ stroke-dasharray: 20 80; animation: scan 6s linear infinite; }}
        @keyframes scan {{ to {{ stroke-dashoffset: -100; }} }}
        @media (prefers-reduced-motion: reduce) {{ .accent {{ animation: none; stroke-dasharray: none; }} }}
      </style>
      <rect width="980" height="236" rx="20" fill="#0b1020"/>
      <text x="30" y="38" fill="#b3bed1" font-size="14" letter-spacing="1.4">{title}</text>
      {''.join(cards)}
    </svg>\n'''


def main():
    owner = os.environ.get("GITHUB_REPOSITORY_OWNER", "").strip()
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", owner):
        raise SystemExit("Run this script in GitHub Actions, or set GITHUB_REPOSITORY_OWNER to your username.")
    user = get_json(f"/users/{quote(owner, safe='')}")
    repositories = get_repositories(owner)
    owned_public = [
        repo for repo in repositories
        if not repo.get("private", False)
        and repo.get("owner", {}).get("login", "").lower() == owner.lower()
    ]
    public_repos = int(user["public_repos"])
    followers = int(user["followers"])
    stars = sum(int(repo.get("stargazers_count", 0)) for repo in owned_public if not repo.get("fork"))
    readme_path = ROOT / "README.md"
    original = readme_path.read_text(encoding="utf-8")
    readme = replace_section(
        original,
        "PROFILE-LINKS",
        f'<p align="center"><a href="https://github.com/{owner}">GitHub @{owner}</a> · '
        f'<a href="https://github.com/{owner}?tab=repositories">Explore my repositories</a></p>',
    )
    readme = replace_section(
        readme,
        "PROFILE-STATS",
        f"**{public_repos:,} public {'repository' if public_repos == 1 else 'repositories'} · "
        f"{followers:,} {'follower' if followers == 1 else 'followers'} · "
        f"{stars:,} {'star' if stars == 1 else 'stars'} on original repositories**\n\n"
        "_Public data only. Stars exclude forked repositories. Refreshed by GitHub Actions._",
    )
    stats = render_stats(owner, public_repos, followers, stars)
    # Network calls and marker checks must succeed before any output is changed.
    (ROOT / "assets" / "stats.svg").write_text(stats, encoding="utf-8")
    readme_path.write_text(readme, encoding="utf-8")
    print("Updated public activity and profile links.")


if __name__ == "__main__":
    try:
        main()
    except (HTTPError, URLError, ValueError, KeyError) as error:
        # Avoid dumping response bodies or request headers to workflow logs.
        raise SystemExit(f"Profile refresh failed ({type(error).__name__}). Previous generated files were retained.") from None
