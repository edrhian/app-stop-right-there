import subprocess
import sys
import os

script_path = os.path.abspath("app.py")

while True:
    result = subprocess.run([sys.executable, script_path])

    if result.returncode != 99:
        break
