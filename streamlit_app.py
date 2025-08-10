import os
import sys

# Add the directory containing run_gui.py to sys.path
run_gui_path = os.path.join(os.path.dirname(__file__), "run_gui.py")
if os.path.exists(run_gui_path):
    sys.path.insert(0, os.path.dirname(run_gui_path))
    import run_gui
else:
    raise FileNotFoundError(f"run_gui.py not found at {run_gui_path}")
