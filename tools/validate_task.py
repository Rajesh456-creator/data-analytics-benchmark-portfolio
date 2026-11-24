"""Re-run each task's reference solution and compare with answer.json."""
import importlib.util, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "tasks"
failed = False
for task in sorted(p for p in ROOT.iterdir() if (p / "reference_solution.py").exists()):
    spec = importlib.util.spec_from_file_location(task.name, task / "reference_solution.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    expected = json.loads((task / "answer.json").read_text())
    if mod.answers != expected:
        failed = True
        print(f"FAIL {task.name}")
        for k in expected:
            if mod.answers.get(k) != expected[k]:
                print(f"  {k}: got {mod.answers.get(k)!r}, expected {expected[k]!r}")
    else:
        print(f"OK   {task.name}")
sys.exit(1 if failed else 0)
