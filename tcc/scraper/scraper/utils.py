from scrapy.http import Response  # type: ignore
from pathlib import Path


def strip_nbsp(string_list: list[str]) -> list[str]:
    return [item.strip().strip("\xa0") for item in string_list if item]


def save_html(self, page, response: Response) -> None:
    filename = f"{page}.html"

    file_path = Path(f"html/{filename}")

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_bytes(response.body)

    self.log(f"Saved file {filename}")
