import subprocess
import sys

scripts = [
    "scripts/ingestion.py",
    "scripts/transform.py",
    "scripts/analyze.py"
]

with open("pipeline_log.txt", "a") as log:
    for script in scripts:
        result = subprocess.run(
            [sys.executable, script],
            stdout=log,
            stderr=log,
            text=True
        )

        if result.returncode != 0:
            print(f"Error running {script}")
            break

    else:
        print("Pipeline complete!")

print("Pipeline complete!")