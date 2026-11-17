"""Rebuild everything from the raw data, then run the checks.

    python code/run_all.py              # ~2 min
    python code/run_all.py --no-checks  # skip code/checks/

Stops at the first script that fails.
"""
import subprocess
import sys
import time
from pathlib import Path

CODE = Path(__file__).resolve().parent
STEPS = ["build_network.py", "distributions.py", "network_structure.py", "node_removal.py",
         "link_removal.py", "compare_webs.py", "compare_webs_stats.py",
         "node_removal_panels.py", "link_removal_panels.py", "explainer.py", "connectivity_panels.py"]
CHECKS = ["checks/verify_cascade.py", "checks/verify_with_igraph.py"]

steps = STEPS + ([] if "--no-checks" in sys.argv else CHECKS)
start = time.time()
for script in steps:
    t = time.time()
    print(f"-> {script}", flush=True)
    subprocess.run([sys.executable, "-W", "ignore", str(CODE / script)], check=True,
                   stdout=subprocess.DEVNULL if script in STEPS else None)
    print(f"   done in {time.time() - t:.0f} s", flush=True)
print(f"all {len(steps)} steps finished in {time.time() - start:.0f} s")
