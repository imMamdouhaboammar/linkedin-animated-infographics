#!/usr/bin/env python3
"""Stable runtime CLI shim.

The implementation lives behind runtime_kernel.main. Public prepare/store flags are
--intent, --stage, and --workspace; keep this shim as the documented interface.
"""
from runtime_kernel import main

if __name__ == "__main__":
    raise SystemExit(main())
