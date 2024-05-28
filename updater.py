import subprocess
import sys

def update_packages(packages):
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])