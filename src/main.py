import logging
import os
import sys
from app import StopRightThereApp
from pathlib import Path
from core.paths import resource_path

logging.basicConfig(
        filename=resource_path("logs/app.log"),
        encoding="UTF-8",
        filemode="a",
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        level=logging.INFO,
    )

blacklist_path = resource_path("data/blacklist.json")

if not os.path.isfile(blacklist_path):
    with open(blacklist_path, "w", encoding="UTF-8") as f:
        f.write("[]")

app = StopRightThereApp()
app.run()
