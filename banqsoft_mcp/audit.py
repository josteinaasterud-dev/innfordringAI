"""Revisjonslogg.

Hvert oppslag mot skyldnerdata logges. Loggen er dokumentasjon på hvem som
slo opp hva og når, og er skrevet for å kunne legges fram ved tilsyn.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class AuditLog:
    def __init__(self, path: str | None = None) -> None:
        self._path = Path(path) if path else None
        if self._path is not None:
            self._path.parent.mkdir(parents=True, exist_ok=True)

    def record(
        self,
        *,
        tool: str,
        arguments: dict[str, Any],
        outcome: str,
        row_count: int | None = None,
        error: str | None = None,
    ) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tool": tool,
            "arguments": arguments,
            "outcome": outcome,
        }
        if row_count is not None:
            entry["row_count"] = row_count
        if error is not None:
            entry["error"] = error

        line = json.dumps(entry, ensure_ascii=False)
        if self._path is not None:
            with self._path.open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")
        else:
            print(line, file=sys.stderr, flush=True)
