from __future__ import annotations

import sys
from pathlib import Path

# Garantiza imports `app.*` al correr pytest desde distintos CWD/IDE.
BACKEND_ROOT = Path(__file__).resolve().parents[2]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))
