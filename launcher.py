"""App launcher"""
import subprocess
import sys
import os


script_path = os.path.abspath("app.py")

# Loop that allows to reset the app (exit - and run again)
while True:
    # Runs the app as a subprocess and waits for it's end
    result = subprocess.run([sys.executable, script_path],check=False)

    if result.returncode != 99:
        break
