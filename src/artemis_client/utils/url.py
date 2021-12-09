def sanitize_url(url: str) -> str:
    url = url.removesuffix("/")
    if not url.startswith("http"):
        url = "https://" + url
    return url
