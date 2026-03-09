from datetime import datetime, timezone
from typing import Optional

COLORS = {
    "green": 0x57F287,
    "red": 0xED4245,
    "yellow": 0xFEE75C,
    "blue": 0x5865F2,
    "gray": 0x95A5A6,
    "orange": 0xE67E22,
}


def build_embed(
    title: str,
    description: str = "",
    color: str = "blue",
    fields: Optional[dict] = None,
    footer: Optional[str] = None,
    timestamp: bool = True,
) -> dict:
    embed: dict = {
        "title": title,
        "color": COLORS.get(color, COLORS["blue"]),
        "fields": [],
    }

    if description:
        embed["description"] = description

    if fields:
        for name, value in fields.items():
            embed["fields"].append({"name": name, "value": str(value), "inline": True})

    if footer:
        embed["footer"] = {"text": footer}

    if timestamp:
        embed["timestamp"] = datetime.now(timezone.utc).isoformat()

    return embed


def format_metrics(metrics: dict) -> dict:
    formatted = {}
    for key, value in metrics.items():
        if isinstance(value, float):
            formatted[key] = f"{value:.4f}"
        else:
            formatted[key] = str(value)
    return formatted
