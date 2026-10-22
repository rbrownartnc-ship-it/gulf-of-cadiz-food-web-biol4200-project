"""Rebuild everything from the raw data, regenerate the notes, run the checks.

    python code/run_all.py              # ~3 min
    python code/run_all.py --no-checks  # skip code/checks/

Stops at the first script that fails.
"""
import subprocess
import sys
import time
from pathlib import Path

CODE = Path(__file__).resolve().parent
STEPS = ["build_network.py", "rq_feasibility.py", "distributions.py", "network_structure.py",
         "node_removal.py", "edge_removal.py", "write_docs.py"]
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
