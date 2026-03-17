#!/usr/bin/env python3
from __future__ import annotations

import uvicorn


if __name__ == "__main__":
    uvicorn.run("app.api:app", host="127.0.0.1", port=8099, reload=False)
