__all__ = ['get_hostnport']


from requests import get


def get_hostnport() -> tuple[str, int]:
    return (
        (r := get(url="https://127.0.0.1/fetch_targets", verify=False).json())[
            "server"
        ],
        int(r["port"]),
    )
