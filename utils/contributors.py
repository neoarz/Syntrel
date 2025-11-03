from io import BytesIO
from math import ceil

import requests
from PIL import Image


def fetch_contributors(owner, repo):
    contributors = []
    page = 1

    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
        params = {"page": page, "per_page": 100}

        headers = {
            "User-Agent": "github-contributors-graph",
            "Accept": "application/vnd.github.v3+json",
        }

        response = requests.get(url, headers=headers, params=params)

        if not response.ok:
            return []

        data = response.json()

        if not data:
            break

        contributors.extend(data)
        page += 1

        if response.headers.get("X-RateLimit-Remaining") == "0":
            break

    return contributors


def download_avatar(avatar_url, size):
    try:
        if "avatars.githubusercontent.com" in avatar_url:
            avatar_url = f"{avatar_url}?s={size}"

        response = requests.get(avatar_url, timeout=10)

        if not response.ok:
            return None

        img = Image.open(BytesIO(response.content))

        if img.size != (size, size):
            img = img.resize((size, size), Image.Resampling.LANCZOS)

        return img

    except Exception:
        return None


def generate_contributors_image(
    owner="neoarz", repo="syntrel", size=64, images_per_row=20
):
    contributors = fetch_contributors(owner, repo)

    if not contributors:
        return None

    images = []

    for contributor in contributors:
        avatar_url = contributor.get("avatar_url")

        if not avatar_url:
            continue

        img = download_avatar(avatar_url, size)

        if img is None:
            continue

        images.append(img)

    if not images:
        return None

    actual_images_per_row = min(len(images), images_per_row)
    width = size * actual_images_per_row
    row_count = ceil(len(images) / images_per_row)
    height = size * row_count

    canvas = Image.new("RGB", (width, height), color="black")

    for idx, img in enumerate(images):
        col = idx % images_per_row
        row = idx // images_per_row
        x = col * size
        y = row * size

        canvas.paste(img, (x, y))

    buffer = BytesIO()
    canvas.save(buffer, "PNG")
    buffer.seek(0)

    return buffer
