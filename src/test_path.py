from core.paths import resource_path
import os

path = resource_path("config/config.yaml")
print("Resolved path:", path)
print("Exists:", os.path.exists(path))
