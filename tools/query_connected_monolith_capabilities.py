#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from axm_institution.connected_monolith import (  # noqa: E402
    ConnectedMonolithCatalog,
    ConnectedMonolithError,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Read a Connected Monolith ZIP as a discovery-only Institution Fabric capability substrate. "
            "This command never executes capability code."
        )
    )
    parser.add_argument("zip", help="Path to a Connected Monolith ZIP")
    parser.add_argument("--expected-zip-sha256")
    parser.add_argument("--address")
    parser.add_argument("--capability")
    parser.add_argument("--module")
    parser.add_argument("--accepts", action="append", default=[])
    parser.add_argument("--provides", action="append", default=[])
    parser.add_argument("--source-status", action="append", default=[])
    parser.add_argument("--limit", type=int, default=50)
    return parser


def main() -> int:
    args = _parser().parse_args()
    if args.limit < 0:
        raise SystemExit("--limit must be >= 0")
    try:
        catalog = ConnectedMonolithCatalog.from_zip(
            args.zip,
            expected_zip_sha256=args.expected_zip_sha256,
        )
        results = catalog.query(
            address=args.address,
            capability=args.capability,
            module=args.module,
            accepts_all=args.accepts,
            provides_all=args.provides,
            adapter_statuses=args.source_status,
        )
    except ConnectedMonolithError as exc:
        print(json.dumps({"error": type(exc).__name__, "message": str(exc)}, indent=2), file=sys.stderr)
        return 2

    if args.limit:
        results = results[: args.limit]
    output = {
        "schema": "axm.institution.connected-monolith-capability-query/v0.1",
        "catalog": catalog.as_summary_dict(),
        "query": {
            "address": args.address,
            "capability": args.capability,
            "module": args.module,
            "accepts_all": args.accepts,
            "provides_all": args.provides,
            "adapter_statuses": args.source_status,
        },
        "result_count": len(results),
        "results": [fact.as_dict() for fact in results],
        "truth_boundary": (
            "Results are discovery facts from the supplied execution fabric. They do not grant Institution Fabric "
            "permission to invoke, install, merge, network, mutate sources, or promote any capability to CANON."
        ),
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
