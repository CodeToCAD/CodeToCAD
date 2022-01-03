import sys
from pathlib import Path
scriptDir = Path(__file__).parent.parent.absolute()
if scriptDir not in sys.path:
    sys.path.insert(0, str(scriptDir))

print("test init run")