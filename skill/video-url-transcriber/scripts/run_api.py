#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import uvicorn


def _inject_repo_root() -> None:
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / "app" / "api.py").exists():
            sys.path.insert(0, str(parent))
            return


_inject_repo_root()


if __name__ == "__main__":
    uvicorn.run("app.api:app", host="127.0.0.1", port=8099, reload=False)
