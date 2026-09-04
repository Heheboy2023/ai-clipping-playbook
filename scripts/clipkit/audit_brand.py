#!/usr/bin/env python3
from clipkit.cli import main

raise SystemExit(main(["audit-brand", *__import__("sys").argv[1:]]))
