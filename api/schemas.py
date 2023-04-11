from dataclasses import dataclass
from pathlib import Path


@dataclass
class Comic:
    image_url: str
    image_name: str
    file_path: Path
    comment: str = ''


@dataclass
class UploadPhoto:
    server_id: int
    photo: str
    hash: str
