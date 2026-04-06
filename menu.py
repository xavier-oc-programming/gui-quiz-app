import os
import subprocess
import sys
from pathlib import Path

from art import LOGO

BASE_DIR = Path(__file__).parent

PATHS = {
    "1": BASE_DIR / "original" / "main.py",
    "2": BASE_DIR / "advanced" / "main.py",
}

while True:
    os.system("cls" if os.name == "nt" else "clear")
    print(LOGO)
    print("Select a build to run:")
    print("  1 — Original")
    print("  2 — Advanced")
    print("  q — Quit")
    choice = input("\nYour choice: ").strip().lower()
    if choice in PATHS:
        path = PATHS[choice]
        subprocess.run([sys.executable, str(path)], cwd=str(path.parent))
    elif choice == "q":
        break
    else:
        print("Invalid choice. Try again.")
