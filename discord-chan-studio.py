#!/usr/bin/env python3
import sys
import os

REAL_SCRIPT = os.path.realpath(__file__)
SCRIPT_DIR = os.path.dirname(REAL_SCRIPT)
sys.path.insert(0, os.path.join(SCRIPT_DIR, "src"))

import studio

if __name__ == "__main__":
    studio.main()
