from datetime import datetime
import os
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from core.settings import PiScannerServerSettings, get_settings
from schemas.scan_schemas import Scan


class ScansHandler:
    __scans_dir: Path

    def __init__(self, scans_dir: str):
        self.__scans_dir = Path(scans_dir).expanduser()

    async def list_scans(self) -> list[Scan]:
        scans: list[Scan] = []

        for scan_file in os.listdir(self.__scans_dir):
            scan_path = os.path.join(self.__scans_dir, scan_file)
            if os.path.isdir(scan_path):
                scans.append(
                    Scan(
                        id=scan_path,
                        created_at=datetime.fromtimestamp(os.path.getctime(scan_path)),
                    )
                )

        return scans


def get_scans_handler(
    scanner_settings: Annotated[PiScannerServerSettings, Depends(get_settings)],
) -> ScansHandler:
    return ScansHandler(scanner_settings.datastore_path)
