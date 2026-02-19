import sys
from pathlib import Path

# Ensure /app/src is on the import path on Spaces
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from careerbot.main import orchestrator  # <-- change 'demo' to your Gradio object name

if __name__ == "__main__":
    orchestrator.launch()
