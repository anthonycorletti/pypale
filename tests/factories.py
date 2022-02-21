def test_email(name: str = "user") -> str:
    return f"{name}@example.com"


def test_base_url(domain_name: str = "example.com") -> str:
    return f"https://{domain_name}"
