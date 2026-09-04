#!/usr/bin/env python3
from clipkit.cli import main
import sys

raise SystemExit(main(["probe", *sys.argv[1:]]))
